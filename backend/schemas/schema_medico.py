from pydantic import BaseModel
from pydantic import BaseModel, field_validator

class MedicoCreate(BaseModel):
    nome: str
    crm: str
    especialidade: str

@field_validator("crm")
@classmethod
def valida_crm(cls, v: str) -> str:
    if not v.isdigit() or len(v) != 6:
        raise ValueError("CRM inválido. Deve conter exatamente 6 dígitos numéricos.")
    return v