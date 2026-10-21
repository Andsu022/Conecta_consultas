from pydantic import BaseModel
from datetime import date, time

class PacienteCreate(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    email: str
