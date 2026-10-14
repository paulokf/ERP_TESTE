# Em backend/app/services/calendar_service.py (linhas de montagem do evento)
doctor_council = f"{doc.council_number or ''}/{doc.council_uf or ''}".strip("/")

event = CalendarEventItem(
    appointment_id=appt.id,
    scheduled_start=appt.scheduled_start,
    scheduled_end=appt.scheduled_end,
    type=appt.type,
    status=appt.status,
    doctor_id=doc.id,
    doctor_name=doc.name,
    doctor_crm=doctor_council if doctor_council else None,
    room_id=appt.room_id,
    patient_id=pat.id,
    patient_name=pat.full_name,
    patient_phone=pat.phone,
    health_insurance=pat.health_insurance_provider
)

