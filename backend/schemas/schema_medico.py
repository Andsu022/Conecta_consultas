from pydantic import BaseModel
from datetime import date, time

class MedicoCreate(BaseModel):
    nome: str
    crm: str
    especialidade: str