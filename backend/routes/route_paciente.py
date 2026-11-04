from backend.schemas.schema_paciente import PacienteCreate

from fastapi import APIRouter, Depends, HTTPException
from backend.dependencies import get_paciente_service
from backend import classes

router = APIRouter(prefix="/paciente", tags=["Pacientes"])

#Paciente
@router.post("", status_code=201)
def cadastrar_paciente(
    paciente: PacienteCreate, 
    paciente_service: classes.Paciente = Depends(get_paciente_service)):

    try: 
        id_paciente = paciente_service.cadastrar_paciente(
            nome = paciente.nome,
            cpf = paciente.cpf,
            data_nascimento = paciente.data_nascimento.isoformat(),
            telefone = paciente.telefone,
            email = paciente.email
        )

    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))
    
    return {"id": id_paciente, "message": "Paciente cadastrado com sucesso"}

@router.get("")
def listar_pacientes(paciente_service: classes.Paciente = Depends(get_paciente_service)):
    return paciente_service.listar_pacientes()