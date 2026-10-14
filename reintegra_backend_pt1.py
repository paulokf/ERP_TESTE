import os

os.makedirs("backend/app/models", exist_ok=True)
os.makedirs("backend/app/routers", exist_ok=True)

models_code = """from sqlalchemy import Column, String, Integer, Text
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

class EvolucaoPEPModel(Base):
    __tablename__ = 'pep_evolucoes'
    id = Column(String(50), primary_key=True, index=True)
    paciente_id = Column(String(50), index=True)
    medico_id = Column(String(50))
    data_registro = Column(String(30))
    anamnese = Column(Text, nullable=True)
    acuidade_od = Column(String(20), nullable=True)
    acuidade_oe = Column(String(20), nullable=True)
    pio_od = Column(String(10), nullable=True)
    pio_oe = Column(String(10), nullable=True)

class LaudoModel(Base):
    __tablename__ = 'pep_laudos'
    id = Column(String(50), primary_key=True, index=True)
    paciente_id = Column(String(50), index=True)
    medico_id = Column(String(50))
    titulo = Column(String(200))
    diagnostico = Column(Text)
    cid10 = Column(String(100), nullable=True)
    data_emissao = Column(String(30))
"""
with open("backend/app/models/core_models.py", "w", encoding="utf-8") as f:
    f.write(models_code)

api_code = """from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.core_models import PacienteModel, AgendamentoModel, EvolucaoPEPModel, LaudoModel
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["Core"])

class PacienteSchema(BaseModel):
    id: str; nome: str; cpf: str; telefone: Optional[str] = None; email: Optional[str] = None

class AgendamentoSchema(BaseModel):
    id: str; paciente_id: str; medico_id: str; medico_nome: str; room_id: int; data_agendamento: str; hora_agendamento: str; tipo: str

class EvolucaoSchema(BaseModel):
    id: str; paciente_id: str; medico_id: str; data_registro: str
    anamnese: Optional[str] = None; acuidade_od: Optional[str] = None; acuidade_oe: Optional[str] = None
    pio_od: Optional[str] = None; pio_oe: Optional[str] = None

class LaudoSchema(BaseModel):
    id: str; paciente_id: str; medico_id: str; titulo: str; diagnostico: str; cid10: Optional[str] = None; data_emissao: str

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

@router.get("/agendamentos")
async def get_agendamentos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AgendamentoModel))
    return result.scalars().all()

@router.post("/agendamentos")
async def create_agendamento(agd: AgendamentoSchema, db: AsyncSession = Depends(get_db)):
    db.add(AgendamentoModel(**agd.dict()))
    await db.commit()
    return {"status": "ok"}

@router.post("/pep/evolucao")
async def save_evolucao(evo: EvolucaoSchema, db: AsyncSession = Depends(get_db)):
    db.add(EvolucaoPEPModel(**evo.dict()))
    await db.commit()
    return {"status": "ok"}

@router.post("/pep/laudos")
async def save_laudo(laudo: LaudoSchema, db: AsyncSession = Depends(get_db)):
    db.add(LaudoModel(**laudo.dict()))
    await db.commit()
    return {"status": "ok"}
"""
with open("backend/app/routers/core_api.py", "w", encoding="utf-8") as f:
    f.write(api_code)

print("Modelos e APIs atualizados.")
