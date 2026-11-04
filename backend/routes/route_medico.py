from backend.schemas.schema_medico import MedicoCreate
from fastapi import APIRouter, Depends, HTTPException
from backend import classes
from backend.dependencies import get_medico_service

router = APIRouter(prefix="/medico", tags=["Médicos"])

#Médico
@router.post("", status_code=201)
def cadastrar_medico(
    medico:MedicoCreate,
    medico_service: classes.Medico = Depends(get_medico_service)):

    try:
        id_medico = medico_service.cadastrar_medico(
            nome = medico.nome,
            crm = medico.crm,
            especialidade = medico.especialidade
        )

    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))

    return {"id": id_medico ,"message": "Médico cadastrado com sucesso"}


@router.get("")
def listar_medicos(medico_service: classes.Medico = Depends(get_medico_service)):
    return medico_service.listar_medicos()