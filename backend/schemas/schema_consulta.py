from pydantic import BaseModel
from datetime import date, time

class ConsultaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    data_consulta: date
    hora_consulta: time
    observacao: str | None = None
    situacao: Literal['agendada', 'realizada', 'cancelada'] = 'agendada'