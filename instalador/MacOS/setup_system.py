#!/usr/bin/env python3
"""
Orquestrador Universal de Instalação e Inicialização do CliniCore ERP
Compatível com Linux, Windows e macOS.
"""

import sys
import os
import time
import subprocess
import shutil
import socket

def print_step(msg: str):
    print(f"\n\033[1;34m===> {msg}\033[0m")

def print_success(msg: str):
    print(f"\033[1;32m✓ {msg}\033[0m")

def print_warn(msg: str):
    print(f"\033[1;33m! {msg}\033[0m")

def print_error(msg: str):
    print(f"\033[1;31m✗ {msg}\033[0m")

def check_command(cmd: str) -> bool:
    return shutil.which(cmd) is not None

def run_cmd(cmd: list, check: bool = True, capture: bool = False):
    try:
        if capture:
            res = subprocess.run(cmd, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return res.stdout.strip()
        else:
            return subprocess.run(cmd, check=check)
    except subprocess.CalledProcessError as e:
        print_error(f"Erro ao executar comando: {' '.join(cmd)}")
        if capture and e.stderr:
            print(e.stderr)
        if check:
            sys.exit(1)
        return None

def check_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('localhost', port)) != 0

def get_docker_compose_cmd() -> list:
    # Testa 'docker compose' (plugin v2)
    try:
        res = subprocess.run(["docker", "compose", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            return ["docker", "compose"]
    except FileNotFoundError:
        pass

    # Testa 'docker-compose' (legado v1)
    if check_command("docker-compose"):
        return ["docker-compose"]

    print_error("Docker Compose não foi encontrado. Instale o Docker e o Docker Compose antes de prosseguir.")
    sys.exit(1)

def ensure_env_file():
    print_step("Verificando arquivos de ambiente (.env)...")
    env_backend = os.path.join("backend", ".env")
    env_frontend = os.path.join("frontend", ".env.local")

    if not os.path.exists(env_backend):
        print_warn(f"Criando {env_backend} padrão...")
        with open(env_backend, "w", encoding="utf-8") as f:
            f.write("DATABASE_URL=postgresql+asyncpg://postgres:postgres@clinicore_postgres:5432/clinicore_db\n")
            f.write("REDIS_URL=redis://clinicore_redis:6379/0\n")
            f.write("SECRET_KEY=clinicore_secret_key_desenvolvimento_local_2026\n")
            f.write("ALGORITHM=HS256\n")
            f.write("ACCESS_TOKEN_EXPIRE_MINUTES=1440\n")
        print_success(f"{env_backend} gerado.")

    if not os.path.exists(env_frontend):
        print_warn(f"Criando {env_frontend} padrão...")
        with open(env_frontend, "w", encoding="utf-8") as f:
            f.write("NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1\n")
        print_success(f"{env_frontend} gerado.")

def wait_for_postgres(compose_cmd: list, max_retries: int = 30):
    print_step("Aguardando o PostgreSQL inicializar e aceitar conexões...")
    for i in range(1, max_retries + 1):
        cmd = compose_cmd + ["exec", "-T", "postgres", "pg_isready", "-U", "postgres"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            print_success(f"PostgreSQL pronto para receber conexões! ({i}s)")
            return True
        time.sleep(1)
        print(f"Tentativa {i}/{max_retries} - aguardando banco de dados...", end="\r")
    
    print_error("\nTempo limite esgotado aguardando o PostgreSQL.")
    sys.exit(1)

def main():
    print("=" * 60)
    print("  INSTALADOR E INICIALIZADOR UNIVERSAL - CLINICORE ERP")
    print("=" * 60)

    # 1. Checagem de Pré-requisitos
    if not check_command("docker"):
        print_error("Docker não encontrado no PATH do sistema. Instale o Docker primeiro.")
        sys.exit(1)

    compose_cmd = get_docker_compose_cmd()
    print_success(f"Docker Compose identificado: {' '.join(compose_cmd)}")

    # 2. Configurações de Ambiente
    ensure_env_file()

    # 3. Subida dos Contêineres
    print_step("Construindo e iniciando contêineres...")
    run_cmd(compose_cmd + ["up", "-d", "--build"])

    # 4. Espera ativa pelo banco
    wait_for_postgres(compose_cmd)

    # 5. Inicialização de Tabelas
    print_step("Sincronizando tabelas do banco de dados...")
    init_db_code = """
import asyncio
from app.database import engine, Base
from app.models.core_models import PatientModel, AppointmentModel, EvolucaoPEPModel, LaudoModel
from app.models.medical_report import MedicalReportModel

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("OK")

asyncio.run(init())
"""
    cmd_init = compose_cmd + ["exec", "-T", "backend", "python", "-c", init_db_code]
    res_init = subprocess.run(cmd_init, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "OK" in res_init.stdout:
        print_success("Estrutura de tabelas garantida no PostgreSQL com sucesso.")
    else:
        print_warn("Aviso ao criar tabelas via script inline. Logs detalhados:")
        print(res_init.stderr or res_init.stdout)

    # 6. Carga de Seeds (Se disponíveis)
    print_step("Executando carga de dados e tabelas de referência...")
    cmd_loader = compose_cmd + ["exec", "-T", "backend", "python", "-m", "app.seeds.loader"]
    res_loader = subprocess.run(cmd_loader, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res_loader.returncode == 0:
        print_success("Seeds básicas carregadas com sucesso.")
    else:
        print_warn("Seeds básicas ignoradas ou módulo loader não registrado.")

    print("\n" + "=" * 60)
    print_success("INSTALAÇÃO E INICIALIZAÇÃO CONCLUÍDAS COM SUCESSO!")
    print("=" * 60)
    print("  • Frontend:  http://localhost:3000")
    print("  • Backend:   http://localhost:8000/docs (Swagger)")
    print("  • PostgreSQL: localhost:5432 (banco: clinicore_db)")
    print("  • Redis:      localhost:6379")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()