from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import date, datetime, timedelta, timezone
from typing import Optional, List
from uuid import UUID

from app.database import get_db
from app.models.appointment import (
    AppointmentModel,
    ReceptionRescheduleQueueModel,
    RescheduleQueueStatus
)
from app.models.patient import PatientModel
from app.models.user import UserModel, UserRole
from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentCancelRequest,
    DoctorAbsenceRequest,
    DoctorAbsenceResponse,
    RescheduleQueueItem,
    CalendarFeedResponse,
    ConfirmationTaskItem,
    ConfirmationActionRequest
)
from app.services.appointment_service import AppointmentConflictService, AppointmentManagementService
from app.services.calendar_service import CalendarService
from app.core.rbac import RequireRoles, get_current_user

router = APIRouter(prefix="/appointments", tags=["Agendamento"])

# 1. Criação de Agendamento (Respeitando a capacidade máxima de 3 consultórios para 15 médicos)
@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.recepcao]))]
)
async def create_appointment(
    payload: AppointmentCreate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Valida paciente
    patient = await db.get(PatientModel, payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não cadastrado.")

    # Valida profissional (permite tanto médico clínico quanto cirurgião)
    doctor = await db.get(UserModel, payload.doctor_id)
    if not doctor or doctor.role not in [UserRole.medico, UserRole.cirurgiao]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O profissional selecionado não possui permissão clínica para realizar atendimentos/cirurgias."
        )

    # Resolve sala (alocação automática entre os 3 consultórios ou validação da sala informada)
    assigned_room = await AppointmentConflictService.resolve_and_validate_room(
        db=db,
        doctor_id=payload.doctor_id,
        patient_id=payload.patient_id,
        requested_room=payload.room_id,
        start_time=payload.scheduled_start,
        end_time=payload.scheduled_end
    )

    new_appointment = AppointmentModel(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        room_id=assigned_room,
        scheduled_start=payload.scheduled_start,
        scheduled_end=payload.scheduled_end,
        type=payload.type,
        notes=payload.notes,
        status="agendado",
        created_by=current_user.id
    )

    db.add(new_appointment)
    try:
        await db.commit()
        await db.refresh(new_appointment)
        return new_appointment
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflito de concorrência detectado: horário ou consultório ocupado simultaneamente por outro operador."
        )

# 2. Alteração / Remarcação Individual
@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponse,
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.recepcao]))]
)
async def update_appointment(
    appointment_id: UUID,
    payload: AppointmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    appointment = await db.get(AppointmentModel, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    if appointment.status in ["cancelado", "concluido"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível alterar um atendimento com status '{appointment.status}'."
        )

    target_doctor_id = payload.doctor_id or appointment.doctor_id
    target_start = payload.scheduled_start or appointment.scheduled_start
    target_end = payload.scheduled_end or appointment.scheduled_end
    target_room = payload.room_id or appointment.room_id

    assigned_room = await AppointmentConflictService.resolve_and_validate_room(
        db=db,
        doctor_id=target_doctor_id,
        patient_id=appointment.patient_id,
        requested_room=target_room,
        start_time=target_start,
        end_time=target_end,
        exclude_appointment_id=appointment.id
    )

    appointment.doctor_id = target_doctor_id
    appointment.room_id = assigned_room
    appointment.scheduled_start = target_start
    appointment.scheduled_end = target_end
    if payload.type:
        appointment.type = payload.type
    if payload.notes is not None:
        appointment.notes = payload.notes
    if payload.status:
        appointment.status = payload.status

    await db.commit()
    await db.refresh(appointment)
    return appointment

# 3. Cancelamento Individual
@router.post(
    "/{appointment_id}/cancel",
    response_model=AppointmentResponse,
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.recepcao, UserRole.medico, UserRole.cirurgiao]))]
)
async def cancel_appointment(
    appointment_id: UUID,
    payload: AppointmentCancelRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AppointmentManagementService.cancel_appointment(
        db=db,
        appointment_id=appointment_id,
        reason=payload.cancellation_reason
    )

# 4. Declarar Ausência Médica (Libera consultórios em lote e popula fila da recepção)
@router.post(
    "/doctor-absence",
    response_model=DoctorAbsenceResponse,
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.rh, UserRole.recepcao]))]
)
async def declare_doctor_absence(
    payload: DoctorAbsenceRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AppointmentManagementService.declare_doctor_absence(
        db=db,
        payload=payload
    )

# 5. Fila de Reagendamento da Recepção (Pacientes impactados por ausências)
@router.get(
    "/reception/reschedule-queue",
    response_model=List[RescheduleQueueItem],
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.recepcao]))]
)
async def list_reschedule_queue(
    status_filter: Optional[str] = "pendente",
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(ReceptionRescheduleQueueModel, PatientModel, UserModel, AppointmentModel)
        .join(PatientModel, ReceptionRescheduleQueueModel.patient_id == PatientModel.id)
        .join(UserModel, ReceptionRescheduleQueueModel.doctor_id == UserModel.id)
        .join(AppointmentModel, ReceptionRescheduleQueueModel.appointment_id == AppointmentModel.id)
    )
    if status_filter:
        query = query.where(ReceptionRescheduleQueueModel.status == status_filter)

    query = query.order_by(AppointmentModel.scheduled_start.asc())
    result = await db.execute(query)
    rows = result.all()

    return [
        RescheduleQueueItem(
            id=queue_entry.id,
            appointment_id=appt.id,
            patient_id=pat.id,
            patient_name=pat.full_name,
            patient_phone=pat.phone,
            doctor_id=doc.id,
            doctor_name=doc.name,
            scheduled_start=appt.scheduled_start,
            reason=queue_entry.reason,
            status=queue_entry.status
        )
        for queue_entry, pat, doc, appt in rows
    ]

# 6. Calendário Semanal
@router.get(
    "/calendar/weekly",
    response_model=CalendarFeedResponse,
    dependencies=[Depends(RequireRoles([
        UserRole.master, UserRole.admin, UserRole.recepcao,
        UserRole.medico, UserRole.cirurgiao, UserRole.anestesiologia, UserRole.instrumentador
    ]))]
)
async def get_weekly_calendar(
    reference_date: Optional[date] = Query(default=None),
    doctor_id: Optional[UUID] = Query(default=None),
    room_id: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    base = reference_date or datetime.now(timezone.utc).date()
    start_week = base - timedelta(days=base.weekday())
    end_week = start_week + timedelta(days=6)

    return await CalendarService.get_calendar_feed(
        db=db,
        start_date=start_week,
        end_date=end_week,
        doctor_id=doctor_id,
        room_id=room_id,
        view_type="weekly"
    )

# 7. Calendário Mensal
@router.get(
    "/calendar/monthly",
    response_model=CalendarFeedResponse,
    dependencies=[Depends(RequireRoles([
        UserRole.master, UserRole.admin, UserRole.recepcao,
        UserRole.medico, UserRole.cirurgiao, UserRole.anestesiologia
    ]))]
)
async def get_monthly_calendar(
    year: int = Query(..., ge=2024, le=2040),
    month: int = Query(..., ge=1, le=12),
    doctor_id: Optional[UUID] = Query(default=None),
    room_id: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    start_month = date(year, month, 1)
    if month == 12:
        end_month = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_month = date(year, month + 1, 1) - timedelta(days=1)

    return await CalendarService.get_calendar_feed(
        db=db,
        start_date=start_month,
        end_date=end_month,
        doctor_id=doctor_id,
        room_id=room_id,
        view_type="monthly"
    )

# 8. Fila de Confirmações D-1 (1 dia antes da consulta)
@router.get(
    "/confirmations/d-minus-one",
    response_model=List[ConfirmationTaskItem],
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.recepcao]))]
)
async def get_pending_d_minus_one_confirmations(
    target_date: Optional[date] = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    return await CalendarService.get_day_minus_one_confirmations(
        db=db,
        target_date=target_date
    )

# 9. Execução da Ação de Confirmação D-1 (Confirmado, reagendar, cancelado, sem resposta)
@router.post(
    "/confirmations/{appointment_id}/action",
    response_model=AppointmentResponse,
    dependencies=[Depends(RequireRoles([UserRole.master, UserRole.admin, UserRole.recepcao]))]
)
async def execute_confirmation_action(
    appointment_id: UUID,
    payload: ConfirmationActionRequest,
    db: AsyncSession = Depends(get_db)
):
    return await CalendarService.process_confirmation_action(
        db=db,
        appointment_id=appointment_id,
        action=payload.action,
        notes=payload.notes
    )

