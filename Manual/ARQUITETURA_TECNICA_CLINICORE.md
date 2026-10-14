# CliniCore ERP — Documentação de Arquitetura de Software e Padrões de Engenharia

**Versão da Plataforma:** 2.6.0-stable  
**Data de Referência Técnica:** 03 de outubro de 2026  
**Público-Alvo:** Engenheiros de Software, Arquitetos de Soluções e Desenvolvedores Full Stack  
**Objetivo:** Padronizar a esteira de desenvolvimento, regras arquiteturais, convenções de código, pipeline de banco de dados e contratos de integração do ecossistema CliniCore.

---

## 1. Visão Geral da Arquitetura do Sistema

O CliniCore é estruturado como um monorepo multi-serviço desacoplado, conteinerizado via Docker Compose, com comunicação síncrona REST (JSON) e mensageria assíncrona baseada em eventos via Redis.
                     [ CLIENTE WEB / NAVEGADOR / ELECTRON ]
                                      │
                             Porta 3000 (HTTP)
                                      ▼
                  ┌────────────────────────────────────────┐
                  │    FRONTEND: Next.js 14 App Router     │
                  │  TypeScript, React 18, Tailwind CSS    │
                  └───────────────────┬────────────────────┘
                                      │
                               fetch / axios (REST)
                               Porta 8000 (HTTP)
                                      ▼
                  ┌────────────────────────────────────────┐
                  │      BACKEND: FastAPI (Python 3.12)    │
                  │ Uvicorn ASGI, Pydantic v2, SQLAlchemy  │
                  └──────────────┬──────────────────┬──────┘
                                 │                  │
            postgresql+asyncpg   │                  │ redis-py (pub/sub & cache)
            Porta 5432           │                  │ Porta 6379
                                 ▼                  ▼
                     ┌─────────────────┐    ┌─────────────────┐
                     │   PostgreSQL    │    │      Redis      │
                     │ (Dados & ACID)  │    │ (Chat / Filas)  │
                     └─────────────────┘    └─────────────────┘

---

## 2. Stack Tecnológica e Versões de Runtimes

### 2.1. Backend
- **Linguagem:** Python 3.12 (CPython runtime em imagem Alpine/Debian slim).
- **Framework Web:** FastAPI >= 0.110.0.
- **Servidor ASGI:** Uvicorn >= 0.28.0 rodando com `uvloop` e `httptools`.
- **ORM / Acesso a Banco:** SQLAlchemy 2.0 Core & Declarative com suporte assíncrono nativo (`ext.asyncio`).
- **Driver de Banco:** `asyncpg` (driver não bloqueante nativo do PostgreSQL em C/Cython).
- **Validação de Tipos & DTOs:** Pydantic v2 (Rust-backed validation core).
- **Controle de Migrações:** Alembic.
- **Cache & Mensageria:** Redis 7.2 com driver `redis-py` (modo assíncrono).

### 2.2. Frontend
- **Framework Core:** Next.js 14.2+ (App Router, Server Components e Client Components seletivos com `'use client'`).
- **Linguagem:** TypeScript 5.4+ (configurado em modo estrito `strict: true`).
- **Biblioteca de Interface:** React 18.2+.
- **Estilização:** Tailwind CSS 3.4+ com plugins de animação (`tailwindcss-animate`).
- **Conjunto de Ícones:** Lucide React.
- **Requisições HTTP:** Fetch API nativa do browser e Axios para chamadas centralizadas com interceptors.

### 2.3. Infraestrutura & Persistência
- **Banco de Dados Relacional:** PostgreSQL 16 (PostGIS opcional para geolocalização).
- **Armazenamento de Filas / Cache:** Redis 7.2 Alpine.
- **Orquestração Local:** Docker Engine 26+ com Docker Compose v2.

---

## 3. Estrutura de Diretórios do Projeto

ERP_Gemini/ ├── docker-compose.yml # Orquestrador multi-contêiner ├── setup_system.py # Script universal de bootstrap e polling ├── install.sh # Wrapper de instalação para Linux/macOS ├── install.ps1 # Wrapper de instalação para Windows PowerShell │ ├── backend/ # Microsserviço de API e Regras de Negócio │ ├── Dockerfile # Build Python 3.12 com dependências de compilação │ ├── requirements.txt # Dependências pip com versões fixadas │ ├── alembic.ini # Configurações do Alembic │ ├── migrations/ # Versões históricas de DDL │ └── app/ │ ├── init.py # Exportações dos módulos centrais │ ├── main.py # Ponto de entrada FastAPI, CORS, middlewares e routers │ ├── database.py # Instância do AsyncEngine, Base e get_db sessionmaker │ ├── models/ # Modelos relacionais (SQLAlchemy) │ │ ├── init.py # Re-export de core_models, medical_report, etc. │ │ ├── core_models.py # Paciente, Agendamento, EvolucaoPEP, Laudo │ │ ├── medical_report.py # Estrutura formal de laudos clínicos e hashing │ │ └── datasus_catalogs.py# Capítulos, Grupos, Categorias e CID-10 │ ├── routers/ # Rotas e controladores REST │ │ ├── init.py │ │ ├── core_api.py # Endpoints CRUD de pacientes, agendamentos e PEP │ │ └── cid10.py # Endpoint do motor de NLP e busca DATASUS │ └── seeds/ # Carga de catálogos e dados de referência │ ├── loader.py # Carga de tabelas TUSS, CBHPM, AMB │ └── import_datasus.py # Carga massiva do dicionário CID-10 │ ├── frontend/ # Aplicação Web (Next.js 14 App Router) │ ├── Dockerfile # Multi-stage build Node 20 │ ├── package.json # Dependências npm │ ├── tsconfig.json # Configurações de tipagem do TypeScript │ ├── tailwind.config.ts # Design tokens e customização de cores │ └── src/ │ ├── app/ │ │ ├── layout.tsx # Root layout com tema e provedores │ │ ├── page.tsx # Redirecionamento inicial │ │ └── dashboard/ │ │ ├── layout.tsx # Shell com sidebar de 9 módulos e topo │ │ ├── agendamento/ │ │ │ └── page.tsx # Grade de salas, semanal, mensal e alocação │ │ └── pep/ │ │ └── page.tsx # Prontuário eletrônico oftalmológico bilateral │ └── lib/ │ ├── api.ts # Cliente Axios configurado com baseURL │ └── utils.ts # Utilitários matemáticos e de formatação │ └── docs/ # Documentação e manuais técnicos └── ARQUITETURA_TECNICA_CLINICORE.md


---

## 4. Padrões de Código e Guia de Estilo (Formatting & Linting)

### 4.1. Convenções de Backend (Python)
- **Guia de Estilo:** Conformidade estrita com a **PEP 8**.
- **Formatador:** `black` configurado para comprimento máximo de linha de **100 caracteres**.
- **Linter & Imports:** `ruff` com ordenação automática de imports via `isort` integrado.
- **Tipagem Estática (Type Hints):** 100% dos parâmetros e retornos de funções assíncronas devem ser anotados:
  ```python
  async def get_patient_by_cpf(cpf: str, db: AsyncSession) -> PatientModel | None:


    Nomenclatura:
        Classes e Modelos: PascalCase (ex.: AppointmentModel, PatientSchema).
        Funções, Métodos e Variáveis: snake_case (ex.: create_agendamento, selected_doctor_id).
        Constantes Globais: UPPER_SNAKE_CASE (ex.: DOCTOR_SLOT_DURATION_MINUTES = 20).

4.2. Convenções de Frontend (TypeScript / React)

    Linter: ESLint com plugins @typescript-eslint e eslint-config-next.
    Formatador: Prettier configurado com printWidth: 100, singleQuote: true, semi: true, trailingComma: "es5".
    Padrão de Componentização:
        Interfaces e Types: PascalCase com nomes semânticos (ex.: interface CalendarAppointment).
        Componentes: PascalCase (ex.: AgendamentoPage).
        Funções utilitárias e hooks: camelCase (ex.: getDisabledTimeSlots, useCurrentWeek).
        Arquivos de Rotas: Estrutura estrita do Next.js App Router (page.tsx, layout.tsx, loading.tsx, error.tsx).
    Gerenciamento de Estado:
        Dados transacionais de servidor: persistidos via API com recarregamento sob demanda (recarregaDados()).
        Estado local de UI: useState e useMemo para cálculos de interseção matemática.
        Proibido o uso de any em tipagens de payloads críticos de negócio.

5. Modelagem de Dados e Regras de Persistência (PostgreSQL)
5.1. Regra de Índices em Chaves Primárias e Campos Únicos

O motor do PostgreSQL cria internamente um índice do tipo B-Tree para qualquer coluna declarada como PRIMARY KEY ou UNIQUE.
Diretriz Crítica: É expressamente proibido declarar index=True junto com primary_key=True ou unique=True no SQLAlchemy, pois isso faz com que o DDL emita comandos duplicados de CREATE INDEX, resultando no erro DuplicateTableError: relation "ix_..._id" already exists.

# Incorreto (causa erro de índice duplicado no PostgreSQL):
id = Column(String(50), primary_key=True, index=True)

# Correto (índice PK criado automaticamente de forma única):
id = Column(String(50), primary_key=True)

# backend/app/models/core_models.py
from sqlalchemy import Column, String, Integer, Text
from app.database import Base

class PatientModel(Base):
    __tablename__ = 'pacientes'
    __table_args__ = {'extend_existing': True}

    id = Column(String(50), primary_key=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(20), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    historico = Column(Text, nullable=True)

class AppointmentModel(Base):
    __tablename__ = 'agendamentos'
    __table_args__ = {'extend_existing': True}

    id = Column(String(50), primary_key=True)
    paciente_id = Column(String(50), nullable=False)
    medico_id = Column(String(50), nullable=False)
    medico_nome = Column(String(150), nullable=False)
    room_id = Column(Integer, nullable=False)
    data_agendamento = Column(String(20), nullable=False)   # Padrão: YYYY-MM-DD
    hora_agendamento = Column(String(10), nullable=False)   # Padrão: HH:mm (ou "00:00" para plantão)
    tipo = Column(String(50), nullable=False)               # 'Consulta' | 'Escala'

class EvolucaoPEPModel(Base):
    __tablename__ = 'pep_evolucoes'
    __table_args__ = {'extend_existing': True}

    id = Column(String(50), primary_key=True)
    paciente_id = Column(String(50), nullable=False)
    medico_id = Column(String(50), nullable=False)
    data_registro = Column(String(30), nullable=False)      # ISO 8601 UTC
    anamnese = Column(Text, nullable=True)
    acuidade_od = Column(String(20), nullable=True)
    acuidade_oe = Column(String(20), nullable=True)
    pio_od = Column(String(10), nullable=True)
    pio_oe = Column(String(10), nullable=True)
    biomicroscopia_od = Column(Text, nullable=True)
    biomicroscopia_oe = Column(Text, nullable=True)
    fundoscopia_od = Column(Text, nullable=True)
    fundoscopia_oe = Column(Text, nullable=True)
    observacoes = Column(Text, nullable=True)               # Limite funcional: 5.000 caracteres

class LaudoModel(Base):
    __tablename__ = 'pep_laudos'
    __table_args__ = {'extend_existing': True}

    id = Column(String(50), primary_key=True)
    paciente_id = Column(String(50), nullable=False)
    medico_id = Column(String(50), nullable=False)
    titulo = Column(String(200), nullable=False)
    diagnostico = Column(Text, nullable=False)
    cid10 = Column(String(100), nullable=True)
    data_emissao = Column(String(30), nullable=False)       # ISO 8601 UTC

6. Algoritmos e Regras de Negócio Críticas
6.1. Validação Matemática de Interseção de Horários (Anti-Conflito)

Consultas médicas possuem duração predeterminada (padrão do CliniCore: 20 minutos).
Dois agendamentos $A$ e $B$ no mesmo consultório ou com o mesmo médico entram em conflito quando seus intervalos de tempo se sobrepõem.

A fórmula booleana de sobreposição de intervalos contínuos $[Start, End)$ aplicada é: $$\text{Conflito} = (Start_A < End_B) \land (End_A > Start_B)$$

Implementação padrão de referência em TypeScript:

export const hasTimeConflict = (
  startA: number, // em minutos decorridos desde as 00:00
  durationA: number,
  startB: number,
  durationB: number
): boolean => {
  const endA = startA + durationA;
  const endB = startB + durationB;
  return startA < endB && endA > startB;
};
6.2. Regras de Exclusividade Diária

    Regra de Exclusividade do Consultório:
    Em uma determinada data $D$, uma sala $S$ só pode ser operada por um único $\text{medico_id}$.
    Regra de Exclusividade do Médico:
    Em uma determinada data $D$, um profissional só pode realizar atendimentos em um único $\text{room_id}$.
    Regra de Pré-Requisito de Plantão (Escala):
    Um paciente só pode ser agendado para o médico $M$ no consultório $S$ e data $D$ se previamente existir um registro de tipo = 'Escala' para o par $(M, S, D)$.

Query SQL de validação cruzada no Backend antes do COMMIT:

SELECT id, medico_id, room_id, medico_nome 
FROM agendamentos 
WHERE data_agendamento = :data_alvo
  AND (
    (medico_id = :novo_medico_id AND room_id != :novo_room_id) OR
    (room_id = :novo_room_id AND medico_id != :novo_medico_id)
  );

7. Conformidade Regulatória (Saúde Digital Brasileira)

A arquitetura do CliniCore foi projetada para cumprir as diretrizes dos seguintes órgãos:

    LGPD (Lei nº 13.709/2018 — Dados Sensíveis de Saúde):
        Dados de saúde (prontuários, laudos e anamnese) são isolados logicamente.
        Trilha de auditoria permanente (audit log) com timestamp UTC e rastreio de operações de escrita.
    CFM (Resolução CFM nº 1.821/2007 — Prontuário Eletrônico):
        Imutabilidade do registro clínico após assinatura. Laudos assinados não aceitam sobrescrita (deve ser criado novo registro ou adendo com histórico).
        Identificação unívoca do profissional: CRM, UF e Especialidade gravados em metadados do documento.
    ANS / Padrão TISS & TUSS:
        Procedimentos armazenados com códigos padronizados da Terminologia Unificada da Saúde Suplementar (ex.: 10101012 para consultas e 41301044 / 41301265 para exames oftalmológicos).
        Suporte à geração de guias no padrão XML TISS 04.xx.
    Ministério da Saúde / DATASUS:
        Catálogo de Classificação Estatística Internacional de Doenças e Problemas Relacionados à Saúde (CID-10) populado em tabelas relacionais com busca fonética/textual via ilike e casamento por palavras-chave.

version: '3.8'

services:
  clinicore_postgres:
    image: postgres:16-alpine
    container_name: clinicore_postgres
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres_secure_password
      POSTGRES_DB: clinicore_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d clinicore_db"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - clinicore_network

  clinicore_redis:
    image: redis:7.2-alpine
    container_name: clinicore_redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - clinicore_network

  clinicore_backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: clinicore_backend
    restart: always
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres_secure_password@clinicore_postgres:5432/clinicore_db
      REDIS_URL: redis://clinicore_redis:6379/0
    ports:
      - "8000:8000"
    depends_on:
      clinicore_postgres:
        condition: service_healthy
    volumes:
      - ./backend/app:/app/app
    networks:
      - clinicore_network

  clinicore_frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: clinicore_frontend
    restart: always
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1
    ports:
      - "3000:3000"
    depends_on:
      - clinicore_backend
    networks:
      - clinicore_network

volumes:
  postgres_data:
  redis_data:

networks:
  clinicore_network:
    driver: bridge

8.2. Ciclo de Polling e Inicialização Segura

Para evitar falhas de inicialização assíncrona onde o backend sobe antes do PostgreSQL completar a fase de recovery, o script de bootstrap setup_system.py executa o comando pg_isready em loop ativo de até 30 segundos antes de invocar a criação de tabelas (Base.metadata.create_all).
9. Comandos Operacionais para o Desenvolvedor

# Iniciar a esteira completa em modo detached
docker compose up -d

# Visualizar logs em tempo real do backend (filtrando por erros)
docker compose logs -f backend

# Executar migração do Alembic no container
docker compose exec backend alembic upgrade head

# Executar shell interativo do banco de dados (psql)
docker compose exec postgres psql -U postgres -d clinicore_db

# Parar serviços sem perder o banco de dados
docker compose down

# Hard Reset completo de desenvolvimento (destrói volumes e recria tabelas)
docker compose down -v && ./install.sh


