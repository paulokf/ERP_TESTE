from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.patient import PatientModel
from app.models.user import UserModel, UserRole
from app.schemas.patient_schema import PatientCreate, PatientUpdate, PatientResponse
from app.core.rbac import RequireRoles, get_current_user

router = APIRouter(prefix="/patients", tags=["Pacientes"])

# Criação de paciente: autorizada para Master, Admin e Recepção
@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.recepcao]))]
)
async def register_patient(
    payload: PatientCreate,
    db: AsyncSession = Depends(get_db)
):
    query = select(PatientModel).where(PatientModel.cpf == payload.cpf)
    if (await db.execute(query)).scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Paciente já cadastrado com este CPF."
        )

    patient_dict = payload.model_dump()
    patient_dict["lgpd_consent_timestamp"] = datetime.now(timezone.utc)

    patient = PatientModel(**patient_dict)
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient

# Busca rápida de pacientes (por CPF ou Nome) para agendamento
@router.get(
    "/search",
    response_model=List[PatientResponse],
    dependencies=[Depends(RequireRoles([
        UserRole.master, 
        UserRole.admin, 
        UserRole.recepcao, 
        UserRole.medico, 
        UserRole.cirurgiao, 
        UserRole.faturamento
    ]))]
)
async def search_patients(
    q: str = Query(..., min_length=2, description="Busca por CPF ou parte do nome"),
    db: AsyncSession = Depends(get_db)
):
    clean_q = q.replace(".", "").replace("-", "")
    query = (
        select(PatientModel)
        .where(
            or_(
                PatientModel.cpf.like(f"%{clean_q}%"),
                PatientModel.full_name.ilike(f"%{q}%")
            )
        )
        .limit(20)
    )
    result = await db.execute(query)
    return result.scalars().all()

# Consulta detalhada de paciente individual
@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    dependencies=[Depends(RequireRoles([
        UserRole.master, 
        UserRole.admin, 
        UserRole.recepcao, 
        UserRole.medico, 
        UserRole.cirurgiao, 
        UserRole.anestesiologia, 
        UserRole.faturamento
    ]))]
)
async def get_patient_details(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    patient = await db.get(PatientModel, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    return patient

