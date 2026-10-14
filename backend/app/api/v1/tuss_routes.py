from fastapi import APIRouter
from typing import List, Dict
from app.constants.tuss_catalog import OPHTHALMIC_TUSS_CATALOG

router = APIRouter(prefix="/catalogs", tags=["Tabelas e Catálogos"])

@router.get("/tuss/ophthalmic")
async def list_ophthalmic_tuss():
    """Retorna a lista de procedimentos TUSS oftalmológicos para autocomplete na recepção."""
    return [
        {"code": code, "description": desc}
        for code, desc in OPHTHALMIC_TUSS_CATALOG.items()
    ]

