from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import UserModel, UserRole
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.core.security import hash_password
from app.core.rbac import RequireRoles

router = APIRouter(prefix="/collaborators", tags=["Colaboradores & RH"])

# Apenas Master, Admin ou RH podem cadastrar colaboradores
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.rh]))]
)
async def create_collaborator(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Checa se o e-mail já existe
    query = select(UserModel).where(UserModel.email == payload.email)
    existing = (await db.execute(query)).scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um colaborador cadastrado com este e-mail."
        )

    # Validação mandatória de CRM para papéis clínicos e cirúrgicos
    clinical_roles = [UserRole.medico, UserRole.cirurgiao, UserRole.anestesiologia]
    if payload.role in clinical_roles and not payload.council_number:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"O número do CRM/Conselho de Classe é obrigatório para o perfil {payload.role.value}."
        )

    new_user = UserModel(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        council_number=payload.council_number,
        council_uf=payload.council_uf.upper() if payload.council_uf else None,
        specialty=payload.specialty,
        is_active=True
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Listagem filtrada por papel operacional
@router.get(
    "/",
    response_model=List[UserResponse],
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.recepcao, UserRole.rh]))]
)
async def list_collaborators(
    role: Optional[UserRole] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(UserModel).where(UserModel.is_active == True)
    if role:
        query = query.where(UserModel.role == role)
    
    query = query.order_by(UserModel.name.asc())
    result = await db.execute(query)
    return result.scalars().all()

