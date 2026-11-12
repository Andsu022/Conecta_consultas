from pydantic import BaseModel, field_validator, Field
from datetime import date, time
from typing import Literal

class ConsultaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    data_consulta: date
    hora_consulta: time
    observacao: str | None = None
    situacao: Literal['agendada', 'realizada', 'cancelada'] = 'agendada'

    @field_validator("data_consulta")
    @classmethod
    def valida_data_consulta(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("A data da consulta não pode ser anterior à data atual.")
        return v

