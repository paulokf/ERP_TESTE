from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from fastapi import HTTPException, status

from app.models.appointment import AppointmentModel, ReceptionRescheduleQueueModel, RescheduleQueueStatus
from app.models.patient import PatientModel
from app.models.user import UserModel
from app.schemas.appointment_schema import DoctorAbsenceRequest, DoctorAbsenceResponse

PHYSICAL_ROOMS: List[str] = ["consultorio_1", "consultorio_2", "consultorio_3"]
MAX_SIMULTANEOUS_ROOMS = 3

class AppointmentConflictService:
    @staticmethod
    def normalize_utc(dt: datetime) -> datetime:
        """Garante que a data esteja explicitamente em UTC."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @classmethod
    async def resolve_and_validate_room(
        cls,
        db: AsyncSession,
        doctor_id: UUID,
        patient_id: UUID,
        requested_room: Optional[str],
        start_time: datetime,
        end_time: datetime,
        exclude_appointment_id: Optional[UUID] = None
    ) -> str:
        start_utc = cls.normalize_utc(start_time)
        end_utc = cls.normalize_utc(end_time)

        if start_utc >= end_utc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O horário de início do agendamento deve ser estritamente anterior ao horário de término."
            )

        # Base de sobreposição: (InícioExistente < FimNovo) AND (FimExistente > InícioNovo)
        overlap_condition = and_(
            AppointmentModel.scheduled_start < end_utc,
            AppointmentModel.scheduled_end > start_utc,
            AppointmentModel.status != "cancelado"  # Agendamentos cancelados liberam a vaga
        )

        # 1. Checar se o médico já está atendendo nesse intervalo
        doctor_conflict_query = select(AppointmentModel).where(
            AppointmentModel.doctor_id == doctor_id,
            overlap_condition
        )
        if exclude_appointment_id:
            doctor_conflict_query = doctor_conflict_query.where(AppointmentModel.id != exclude_appointment_id)
        
        doctor_conflict = (await db.execute(doctor_conflict_query)).scalars().first()
        if doctor_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conflito de agenda: o médico já possui um atendimento marcado neste horário."
            )

        # 2. Checar se o paciente já está em outro atendimento no mesmo intervalo
        patient_conflict_query = select(AppointmentModel).where(
            AppointmentModel.patient_id == patient_id,
            overlap_condition
        )
        if exclude_appointment_id:
            patient_conflict_query = patient_conflict_query.where(AppointmentModel.id != exclude_appointment_id)

        patient_conflict = (await db.execute(patient_conflict_query)).scalars().first()
        if patient_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conflito de agenda: o paciente já possui outro procedimento marcado neste mesmo horário."
            )

        # 3. Descobrir quais dos 3 consultórios físicos estão ocupados no momento
        occupied_rooms_query = select(AppointmentModel.room_id).where(
            AppointmentModel.room_id.in_(PHYSICAL_ROOMS),
            overlap_condition
        )
        if exclude_appointment_id:
            occupied_rooms_query = occupied_rooms_query.where(AppointmentModel.id != exclude_appointment_id)

        occupied_rooms_result = await db.execute(occupied_rooms_query)
        occupied_rooms = set(occupied_rooms_result.scalars().all())

        # 4. Resolução da Sala
        if requested_room in [None, "auto", ""]:
            # Alocação Automática entre os consultórios livres
            free_rooms = [r for r in PHYSICAL_ROOMS if r not in occupied_rooms]
            if not free_rooms:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Capacidade máxima atingida: os 3 consultórios físicos da clínica estão ocupados neste horário."
                )
            return free_rooms[0]
        else:
            # Sala específica solicitada
            if requested_room not in PHYSICAL_ROOMS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Consultório inválido '{requested_room}'. Opções físicas disponíveis: {PHYSICAL_ROOMS}"
                )
            if requested_room in occupied_rooms:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"O consultório '{requested_room}' já está ocupado por outro médico neste intervalo."
                )
            return requested_room

