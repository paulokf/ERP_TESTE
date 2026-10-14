import os
import json
from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.medical_report import MedicalReportModel
from app.models.user import UserModel, UserRole
from app.schemas.report_schema import MedicalReportCreateMeta, MedicalReportResponse
from app.services.report_service import MedicalReportService
from app.core.rbac import RequireRoles, get_current_user, get_current_user_flexible

router = APIRouter(prefix="/patients", tags=["Prontuário - Laudos e Exames"])


# ==============================================================================
# 1. EMITIR LAUDO MÉDICO COM UPLOAD DE ARQUIVO/IMAGEM
# ==============================================================================
@router.post(
    "/{patient_id}/reports",
    response_model=MedicalReportResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RequireRoles([
        UserRole.master, 
        UserRole.admin, 
        UserRole.medico, 
        UserRole.cirurgiao
    ]))]
)
async def create_patient_medical_report(
    patient_id: UUID,
    metadata_json: str = Form(..., description="JSON serializado correspondente a MedicalReportCreateMeta"),
    file: UploadFile = File(..., description="Imagem do exame (JPG, PNG, WEBP) ou PDF"),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        data_dict = json.loads(metadata_json)
        data_dict["patient_id"] = patient_id
        meta = MedicalReportCreateMeta(**data_dict)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Parâmetros de metadados do laudo inválidos: {str(exc)}"
        )

    report = await MedicalReportService.create_report(
        db=db,
        doctor=current_user,
        meta=meta,
        file=file
    )

    doctor_council = f"{current_user.council_number or ''}/{current_user.council_uf or ''}".strip("/")

    return MedicalReportResponse(
        id=report.id,
        patient_id=report.patient_id,
        doctor_id=report.doctor_id,
        doctor_name=current_user.name,
        doctor_crm=doctor_council if doctor_council else None,
        appointment_id=report.appointment_id,
        tuss_code=report.tuss_code,
        procedure_name=report.procedure_name,
        cid10_code=report.cid10_code,
        cid10_description=report.cid10_description,
        eye_laterality=report.eye_laterality,
        clinical_indication=report.clinical_indication,
        report_body=report.report_body,
        diagnostic_conclusion=report.diagnostic_conclusion,
        file_name=report.file_name,
        file_content_type=report.file_content_type,
        file_size_bytes=report.file_size_bytes,
        sha256_hash=report.sha256_hash,
        signed_at=report.signed_at,
        created_at=report.created_at
    )


# ==============================================================================
# 2. LISTAR HISTÓRICO DE LAUDOS DO PACIENTE (PRONTUÁRIO)
# ==============================================================================
@router.get(
    "/{patient_id}/reports",
    response_model=List[MedicalReportResponse],
    dependencies=[Depends(RequireRoles([
        UserRole.master, 
        UserRole.admin, 
        UserRole.medico, 
        UserRole.cirurgiao,
        UserRole.anestesiologia, 
        UserRole.recepcao, 
        UserRole.faturamento
    ]))]
)
async def list_patient_medical_reports(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(MedicalReportModel, UserModel)
        .join(UserModel, MedicalReportModel.doctor_id == UserModel.id)
        .where(MedicalReportModel.patient_id == patient_id)
        .order_by(MedicalReportModel.signed_at.desc())
    )
    result = await db.execute(query)
    rows = result.all()

    response_items = []
    for rep, doc in rows:
        council = f"{doc.council_number or ''}/{doc.council_uf or ''}".strip("/")
        response_items.append(
            MedicalReportResponse(
                id=rep.id,
                patient_id=rep.patient_id,
                doctor_id=rep.doctor_id,
                doctor_name=doc.name,
                doctor_crm=council if council else None,
                appointment_id=rep.appointment_id,
                tuss_code=rep.tuss_code,
                procedure_name=rep.procedure_name,
                cid10_code=rep.cid10_code,
                cid10_description=rep.cid10_description,
                eye_laterality=rep.eye_laterality,
                clinical_indication=rep.clinical_indication,
                report_body=rep.report_body,
                diagnostic_conclusion=rep.diagnostic_conclusion,
                file_name=rep.file_name,
                file_content_type=rep.file_content_type,
                file_size_bytes=rep.file_size_bytes,
                sha256_hash=rep.sha256_hash,
                signed_at=rep.signed_at,
                created_at=rep.created_at
            )
        )

    return response_items


# ==============================================================================
# 3. VISUALIZAR / BAIXAR A IMAGEM DO LAUDO (AUTENTICAÇÃO FLEXÍVEL)
# ==============================================================================
@router.get("/{patient_id}/reports/{report_id}/image")
async def download_report_image(
    patient_id: UUID,
    report_id: UUID,
    token: Optional[str] = Query(None, description="Token JWT para renderização direta em tags <img> ou <iframe>"),
    current_user: UserModel = Depends(get_current_user_flexible),
    db: AsyncSession = Depends(get_db)
):
    # RBAC: Verifica papéis permitidos para acesso à imagem do laudo
    allowed_roles = {
        UserRole.master, 
        UserRole.admin, 
        UserRole.medico, 
        UserRole.cirurgiao,
        UserRole.anestesiologia, 
        UserRole.recepcao, 
        UserRole.faturamento
    }
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acesso não autorizado para esta função."
        )

    report = await db.get(MedicalReportModel, report_id)
    if not report or report.patient_id != patient_id:
        raise HTTPException(status_code=404, detail="Laudo não localizado para este paciente.")

    if not os.path.exists(report.file_path):
        raise HTTPException(
            status_code=status.HTTP_410_GONE, 
            detail="O arquivo físico do laudo não se encontra no armazenamento do servidor."
        )

    return FileResponse(
        path=report.file_path,
        media_type=report.file_content_type,
        filename=report.file_name,
        headers={"Content-Disposition": f'inline; filename="{report.file_name}"'}
    )

