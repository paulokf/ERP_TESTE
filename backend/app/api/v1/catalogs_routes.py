from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List

from app.database import get_db
from app.models.medical_catalogs import CID10Model, ProcedureCatalogModel
from app.schemas.catalog_schema import CID10Response, ProcedureCatalogResponse
from app.core.rbac import get_current_user

router = APIRouter(prefix="/catalogs", tags=["Catálogos Oficiais (AMB, CBHPM, TUSS, CID10)"])

# Busca de CID-10 para emissão de Laudos e Atestados
@router.get("/cid10", response_model=List[CID10Response])
async def search_cid10(
    q: str = Query(..., min_length=2, description="Código (ex: H25) ou termo da patologia"),
    db: AsyncSession = Depends(get_db),
    _user = Depends(get_current_user)
):
    query = (
        select(CID10Model)
        .where(
            CID10Model.is_active == True,
            or_(
                CID10Model.code.ilike(f"{q}%"),
                CID10Model.description.ilike(f"%{q}%")
            )
        )
        .order_by(CID10Model.code.asc())
        .limit(25)
    )
    result = await db.execute(query)
    return result.scalars().all()

# Busca cruzada de Procedimentos (TUSS, CBHPM ou AMB) para Agendamento e Guias TISS
@router.get("/procedures", response_model=List[ProcedureCatalogResponse])
async def search_procedures(
    q: str = Query(..., min_length=2, description="Código TUSS/CBHPM/AMB ou descrição"),
    category: str = Query(None, description="Filtro opcional: consulta, exame, cirurgia, laser"),
    db: AsyncSession = Depends(get_db),
    _user = Depends(get_current_user)
):
    clean_code = q.replace(".", "").replace("-", "")
    filters = [
        ProcedureCatalogModel.is_active == True,
        or_(
            ProcedureCatalogModel.tuss_code.like(f"{clean_code}%"),
            ProcedureCatalogModel.cbhpm_code.ilike(f"%{q}%"),
            ProcedureCatalogModel.amb_code.ilike(f"%{q}%"),
            ProcedureCatalogModel.description.ilike(f"%{q}%")
        )
    ]
    if category:
        filters.append(ProcedureCatalogModel.category == category)

    query = select(ProcedureCatalogModel).where(*filters).order_by(ProcedureCatalogModel.description.asc()).limit(25)
    result = await db.execute(query)
    return result.scalars().all()

