from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.appointment import Appointment  # ajuste se sua entidade tiver outro nome
from app.schemas.appointment import AppointmentCreate

MAX_PHYSICAL_ROOMS = 3

class ScheduleService:
    @staticmethod
    def validate_room_and_doctor_availability(
        db: Session,
        room_id: int,
        doctor_id: str,
        start_time: datetime,
        duration_minutes: int = 30
    ) -> bool:
        end_time = start_time + timedelta(minutes=duration_minutes)

        # 1. Verifica se o médico já possui compromisso no mesmo horário
        doctor_conflict = db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status != "CANCELLED",
            Appointment.start_time < end_time,
            Appointment.end_time > start_time
        ).first()

        if doctor_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Médico já possui agendamento entre {doctor_conflict.start_time} e {doctor_conflict.end_time}."
            )

        # 2. Verifica se a sala específica está ocupada
        room_conflict = db.query(Appointment).filter(
            Appointment.room_id == room_id,
            Appointment.status != "CANCELLED",
            Appointment.start_time < end_time,
            Appointment.end_time > start_time
        ).first()

        if room_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Consultório {room_id} já está ocupado neste horário."
            )

        # 3. Trava física global: nunca mais que 3 consultórios ativos em simultâneo
        active_rooms_count = db.query(Appointment.room_id).filter(
            Appointment.status != "CANCELLED",
            Appointment.start_time < end_time,
            Appointment.end_time > start_time
        ).distinct().count()

        if active_rooms_count >= MAX_PHYSICAL_ROOMS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Limite físico da clínica atingido (máximo de 3 consultórios em uso simultâneo)."
            )

        return True

    @staticmethod
    def cancel_batch_by_doctor_absence(
        db: Session,
        doctor_id: str,
        absence_date: datetime.date,
        reason: str
    ) -> int:
        """
        Cancela todos os agendamentos de um médico específico em um dia determinado
        e gera a flag para a recepção realizar a remarcação ativa.
        """
        start_day = datetime.combine(absence_date, datetime.min.time())
        end_day = datetime.combine(absence_date, datetime.max.time())

        appointments = db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status != "CANCELLED",
            Appointment.start_time >= start_day,
            Appointment.start_time <= end_day
        ).all()

        count = len(appointments)
        for appt in appointments:
            appt.status = "CANCELLED_DOCTOR_ABSENCE"
            appt.cancellation_reason = reason
            appt.requires_rescheduling = True

        db.commit()
        return count
