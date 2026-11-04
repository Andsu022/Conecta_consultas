from backend.schemas.schema_consulta import ConsultaCreate

from fastapi import APIRouter, Depends, HTTPException
from backend import classes
from backend.dependencies import get_consulta_service

router = APIRouter(prefix="/consulta", tags=["Consultas"])

#Consulta
@router.post("", status_code=201)
def agendar_consulta(
    consulta:ConsultaCreate,
    consulta_service: classes.Consulta = Depends(get_consulta_service)):

    try:
        id_consulta = consulta_service.agendar_consulta(
            paciente_id = consulta.paciente_id,
            medico_id = consulta.medico_id,
            data_consulta = consulta.data_consulta.isoformat(),
            hora_consulta = consulta.hora_consulta.isoformat(),
            observacao = consulta.observacao,
            situacao = consulta.situacao
        )

    except LookupError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))
    
    return {"id": id_consulta, "message": "Consulta agendada com sucesso"}

@router.get("/{id}")
def buscar_consulta(id: int, consulta_service: classes.Consulta = Depends(get_consulta_service)):
    consulta = consulta_service.buscar_consulta(id)
    if consulta is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada !")

    return consulta