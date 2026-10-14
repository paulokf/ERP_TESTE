from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AgendamentoBaseSchema(BaseModel):
    paciente_nome: str
    paciente_cpf: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    consultorio_id: int = Field(..., ge=1, le=3, description="Trava dos 3 consultórios físicos")
    medico_id: int
    data_hora: datetime
    procedimento_tuss: str
    tipo_atendimento: str = "PARTICULAR"
    convenio_operadora: Optional[str] = None
    carteirinha_numero: Optional[str] = None
    observacoes: Optional[str] = None

class AgendamentoCreateSchema(AgendamentoBaseSchema):
    pass

class AgendamentoUpdateSchema(BaseModel):
    paciente_nome: Optional[str] = None
    paciente_cpf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    consultorio_id: Optional[int] = Field(None, ge=1, le=3)
    medico_id: Optional[int] = None
    data_hora: Optional[datetime] = None
    procedimento_tuss: Optional[str] = None
    tipo_atendimento: Optional[str] = None
    convenio_operadora: Optional[str] = None
    carteirinha_numero: Optional[str] = None
    status: Optional[str] = None
    motivo_cancelamento: Optional[str] = None

class AgendamentoResponseSchema(AgendamentoBaseSchema):
    id: int
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
