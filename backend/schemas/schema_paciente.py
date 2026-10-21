from pydantic import BaseModel, EmailStr, Field, field_validator

class PacienteCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    cpf: str
    data_nascimento: date
    telefone: str = Field(min_length=8, max_length=20)
    email: EmailStr

    @field_validator("cpf")
    @classmethod
    def normaliza_cpf(cls, v:str)->str:
        digitos = "".join(c for c in v if c.isdigit())
        if len(digitos) != 11:
            raise ValueError("CPF deve ter 11 dígitos.")
        return digitos
