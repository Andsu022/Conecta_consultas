# Criação de rotas e API REST no FastAPI
import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.db import init_db
from backend.routes import route_consulta, route_medico, route_paciente

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"]
)

#Paciente
@app.post("/paciente", status_code=201)
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

@app.get("/paciente")
def listar_pacientes(paciente_service: classes.Paciente = Depends(get_paciente_service)):
    return paciente_service.listar_pacientes()

#Médico
@app.post("/medico", status_code=201)
def cadastrar_medico(
    medico:MedicoCreate,
    medico_service: classes.Medico = Depends(get_medico_service)):

    try:
        medico_service.cadastrar_medico(
            nome = medico.nome,
            crm = medico.crm,
            especialidade = medico.especialidade
        )

    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))

    return {"message": "Médico cadastrado com sucesso"}

@app.get("/medico")
def listar_medicos(medico_service: classes.Medico = Depends(get_medico_service)):
    return medico_service.listar_medicos()
