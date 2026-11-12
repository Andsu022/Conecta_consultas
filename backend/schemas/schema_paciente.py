from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date
import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat

def _cpf_valido(cpf: str) -> bool:
    if len(cpf)!= 11 or cpf[0] * 11 == cpf:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = ((soma * 10) % 11) % 10
        if int(cpf[i]) != digito:
            return False
    return True

class PacienteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(min_length=2, max_length=120)
    cpf: str
    data_nascimento: date
    telefone: str = Field(min_length=8, max_length=20)
    email: EmailStr

    @field_validator("cpf")
    @classmethod
    def normaliza_cpf(cls, v:str)->str:
        digitos = "".join(c for c in v if c.isdigit())
        if not _cpf_valido(digitos):
            raise ValueError("CPF inválido")
        return digitos

    @field_validator("telefone")
    @classmethod
    def normaliza_telefone(cls, v:str)->str:
        try:
            phone_obj = phonenumbers.parse(v, "BR")
        except NumberParseException:
            raise ValueError("Número de telefone inválido")
        if not phonenumbers.is_valid_number(phone_obj):
            raise ValueError("Número de telefone inválido")
        return phonenumbers.format_number(phone_obj, PhoneNumberFormat.E164)

    @field_validator("data_nascimento")
    @classmethod
    def valida_nascimento(cls, v: date) -> date:
        hoje = date.today()
        if v > hoje:
            raise ValueError("Data de nascimento não pode ser futura.")
        if v.year < hoje.year - 120:
            raise ValueError("Data de nascimento inválida.")
        return v

    @field_validator("email")
    @classmethod
    def normaliza_email(cls, v: str) -> str:
        return v.lower()
    
    