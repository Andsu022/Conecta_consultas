from schemas.schema_consulta import ConsultaCreate
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException
from backend.dependencies import get_consulta_service
from fastapi.responses import JSONResponse


#Consulta
@app.post("/consulta", status_code=201)
def agendar_consulta(
    consulta:ConsultaCreate,
    consulta_service: classes.Consulta = Depends(get_consulta_service)):

    try:
        consulta_service.agendar_consulta(
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
    
    return {"message": "Consulta agendada com sucesso"}

@app.get("/consulta/{id}")
def listar_consultas(consulta_service: classes.Consulta = Depends(get_consulta_service)):
    return consulta_service.listar_consultas()