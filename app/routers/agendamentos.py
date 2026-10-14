from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.agendamento import Agendamento
from app.schemas.agendamento import AgendamentoCreateSchema, AgendamentoUpdateSchema, AgendamentoResponseSchema

router = APIRouter(prefix="/api/v1/agendamentos", tags=["Agendamentos"])

@router.post("/", response_model=AgendamentoResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_agendamento(payload: AgendamentoCreateSchema, db: Session = Depends(get_db)):
    # 1. Trava de Sala
    conflito_sala = db.query(Agendamento).filter(
        Agendamento.consultorio_id == payload.consultorio_id,
        Agendamento.data_hora == payload.data_hora,
        Agendamento.status != "CANCELADO"
    ).first()
    if conflito_sala:
        raise HTTPException(status_code=409, detail=f"O Consultório {payload.consultorio_id} já está ocupado neste horário.")

    # 2. Trava de Médico
    conflito_medico = db.query(Agendamento).filter(
        Agendamento.medico_id == payload.medico_id,
        Agendamento.data_hora == payload.data_hora,
        Agendamento.status != "CANCELADO"
    ).first()
    if conflito_medico:
        raise HTTPException(status_code=409, detail="O médico selecionado já possui atendimento neste horário.")

    novo = Agendamento(**payload.dict(), status="AGENDADO", created_at=datetime.utcnow())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.put("/{agendamento_id}", response_model=AgendamentoResponseSchema)
def alterar_agendamento(agendamento_id: int, payload: AgendamentoUpdateSchema, db: Session = Depends(get_db)):
    item = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    if payload.consultorio_id and payload.data_hora:
        conflito_sala = db.query(Agendamento).filter(
            Agendamento.id != agendamento_id,
            Agendamento.consultorio_id == payload.consultorio_id,
            Agendamento.data_hora == payload.data_hora,
            Agendamento.status != "CANCELADO"
        ).first()
        if conflito_sala:
            raise HTTPException(status_code=409, detail=f"O Consultório {payload.consultorio_id} já está ocupado.")

    if payload.medico_id and payload.data_hora:
        conflito_medico = db.query(Agendamento).filter(
            Agendamento.id != agendamento_id,
            Agendamento.medico_id == payload.medico_id,
            Agendamento.data_hora == payload.data_hora,
            Agendamento.status != "CANCELADO"
        ).first()
        if conflito_medico:
            raise HTTPException(status_code=409, detail="O médico selecionado já possui atendimento neste horário.")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(item, k, v)

    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{agendamento_id}")
def remover_ou_inativar(agendamento_id: int, motivo: Optional[str] = None, db: Session = Depends(get_db)):
    item = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    # Regra CFM / Auditoria: se já tiver histórico ou prontuário gerado, inativa em vez de apagar
    tem_prontuario = getattr(item, "prontuario_gerado", False)
    if tem_prontuario:
        item.status = "CANCELADO"
        item.motivo_cancelamento = motivo or "Cancelamento administrativo / CFM"
        item.updated_at = datetime.utcnow()
        db.commit()
        return {"action": "INATIVADO", "message": "Atendimento cancelado e mantido para auditoria."}

    db.delete(item)
    db.commit()
    return {"action": "EXCLUIDO", "message": "Horário liberado na grade."}
