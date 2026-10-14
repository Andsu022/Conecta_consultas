# Criação de rotas e API REST no FastAPI
from typing import Literal
from backend import classes
from fastapi import FastAPI, HTTPException, Depends

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date, time

import sqlite3
from contextlib import asynccontextmanager
from backend.db import DB_PATH, init_db, get_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    try:
        init_db(connection)
    finally:
        connection.close()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"]
)


class PacienteCreate(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    email: str

class MedicoCreate(BaseModel):
    nome: str
    crm: str
    especialidade: str

class ConsultaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    data_consulta: date
    hora_consulta: time
    observacao: str | None = None
    situacao: Literal['agendada', 'realizada', 'cancelada'] = 'agendada'

# Dependencias de conexão da requisição
def get_paciente_service(connection: sqlite3.Connection = Depends(get_connection)):
    return classes.Paciente(connection)

def get_medico_service(connection: sqlite3.Connection = Depends(get_connection)):
    return classes.Medico(connection)

def get_consulta_service(connection: sqlite3.Connection = Depends(get_connection)):
    return classes.Consulta(connection)

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
    return paciente_service.listar_paciente()

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