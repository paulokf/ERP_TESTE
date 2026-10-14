import os
import hashlib
from uuid import UUID, uuid4
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.medical_report import MedicalReportModel
from app.models.patient import PatientModel
from app.models.user import UserModel, UserRole
from app.models.medical_catalogs import CID10Model
from app.schemas.report_schema import MedicalReportCreateMeta

# Diretório seguro para anexos de prontuário (configurável via env/settings)
REPORTS_STORAGE_DIR = os.getenv("CLINICORE_REPORTS_DIR", "/var/lib/clinicore/medical_reports")
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB por arquivo

class MedicalReportService:
    @classmethod
    async def create_report(
        cls,
        db: AsyncSession,
        doctor: UserModel,
        meta: MedicalReportCreateMeta,
        file: UploadFile
    ) -> MedicalReportModel:
        # 1. Validação de Papel: Apenas Médico ou Cirurgião pode emitir e assinar laudo
        if doctor.role not in [UserRole.medico, UserRole.cirurgiao]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas médicos com registro no CRM/RQE podem emitir laudos oftalmológicos."
            )

        # 2. Validação do Paciente
        patient = await db.get(PatientModel, meta.patient_id)
        if not patient or patient.is_deleted:
            raise HTTPException(status_code=404, detail="Paciente não encontrado ou inativo.")

        # 3. Validação do Arquivo / Imagem
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de arquivo não permitido. Formatos aceitos: {ALLOWED_MIME_TYPES}"
            )

        file_bytes = await file.read()
        file_size = len(file_bytes)
        if file_size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O arquivo excede o limite máximo permitido de {MAX_FILE_SIZE_BYTES // (1024*1024)}MB."
            )

        # 4. Cálculo do HASH SHA-256 para auditoria e integridade (exigência CFM)
        sha256_hash = hashlib.sha256(file_bytes).hexdigest()

        # 5. Persistência Segura do Arquivo em Disco
        os.makedirs(REPORTS_STORAGE_DIR, exist_ok=True)
        file_ext = os.path.splitext(file.filename or "")[1].lower()
        if not file_ext:
            file_ext = ".jpg" if "jpeg" in file.content_type else ".png"

        stored_filename = f"{uuid4().hex}_{sha256_hash[:12]}{file_ext}"
        absolute_file_path = os.path.join(REPORTS_STORAGE_DIR, stored_filename)

        with open(absolute_file_path, "wb") as f:
            f.write(file_bytes)

        # 6. Gravação no Prontuário Eletrônico
        new_report = MedicalReportModel(
            patient_id=meta.patient_id,
            doctor_id=doctor.id,
            appointment_id=meta.appointment_id,
            tuss_code=meta.tuss_code,
            procedure_name=meta.procedure_name,
            cid10_code=meta.cid10_code,
            cid10_description=meta.cid10_description,
            eye_laterality=meta.eye_laterality,
            clinical_indication=meta.clinical_indication,
            report_body=meta.report_body,
            diagnostic_conclusion=meta.diagnostic_conclusion,
            file_path=absolute_file_path,
            file_name=file.filename or stored_filename,
            file_content_type=file.content_type,
            file_size_bytes=file_size,
            sha256_hash=sha256_hash,
            is_signed=True,
            signed_at=datetime.now(timezone.utc)
        )

        db.add(new_report)
        await db.commit()
        await db.refresh(new_report)
        return new_report

