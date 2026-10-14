import os
import re

os.makedirs("backend/app/models", exist_ok=True)
os.makedirs("backend/app/routers", exist_ok=True)

# 1. Cria os Modelos de Banco de Dados
with open("backend/app/models/core_models.py", "w", encoding="utf-8") as f:
    f.write("""from sqlalchemy import Column, String, Integer, Text, ForeignKey
from app.database import Base

class PacienteModel(Base):
    __tablename__ = 'pacientes'
    id = Column(String(50), primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(20), unique=True, index=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    historico = Column(Text, nullable=True)

class AgendamentoModel(Base):
    __tablename__ = 'agendamentos'
    id = Column(String(50), primary_key=True, index=True)
    paciente_id = Column(String(50))
    medico_id = Column(String(50))
    medico_nome = Column(String(150))
    room_id = Column(Integer)
    data_agendamento = Column(String(20))
    hora_agendamento = Column(String(10))
    tipo = Column(String(50))
""")

# 2. Cria as Rotas da API
with open("backend/app/routers/core_api.py", "w", encoding="utf-8") as f:
    f.write("""from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.core_models import PacienteModel, AgendamentoModel
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["Core"])

class PacienteSchema(BaseModel):
    id: str
    nome: str
    cpf: str

class AgendamentoSchema(BaseModel):
    id: str
    paciente_id: str
    medico_id: str
    medico_nome: str
    room_id: int
    data_agendamento: str
    hora_agendamento: str
    tipo: str

@router.get("/pacientes")
async def get_pacientes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PacienteModel))
    return result.scalars().all()

@router.post("/pacientes")
async def create_paciente(pac: PacienteSchema, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(select(PacienteModel).where(PacienteModel.id == pac.id))
    if not exists.scalars().first():
        db.add(PacienteModel(**pac.dict()))
        await db.commit()
    return {"status": "ok"}
""")

# 3. Injeta a rota no main.py
main_path = "backend/app/main.py"
if os.path.exists(main_path):
    with open(main_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "core_api.router" not in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "from fastapi" in line:
                lines.insert(i + 1, "from app.routers import core_api")
                break
        for i, line in enumerate(lines):
            if "app.include_router" in line:
                lines.insert(i + 1, "app.include_router(core_api.router)")
                break
        with open(main_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))

# 4. Script para criar as tabelas no PostgreSQL
with open("init_core_db.py", "w", encoding="utf-8") as f:
    f.write("""import asyncio
from app.database import engine, Base
from app.models.core_models import PacienteModel, AgendamentoModel
async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(init())
""")
