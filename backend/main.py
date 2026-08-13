# Criação de rotas e API REST no FastAPI
import classes
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date, time

class Paciente_Create(BaseModel):
    nome: str
    cpf: str
    data_nascimento: str
    telefone: str
    email: str

class Medico_Create(BaseModel):
    nome: str
    crm: str
    especialidade: str

class Consulta_Create(BaseModel):
    paciente_id: int
    medico_id: int
    data_consulta: date
    hora_consulta: time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"]
)

paciente_service = classes.Paciente()
medico_service = classes.Medico()
consulta_service = classes.Consulta()

@app.post("/paciente", status_code=201)
def cadastrar_paciente(paciente:Paciente_Create):
    try: 
        paciente_service.cadastrar_paciente(
            nome = paciente.nome,
            cpf = paciente.cpf,
            data_nascimento = paciente.data_nascimento,
            telefone = paciente.telefone,
            email = paciente.email
        )
        return {"message": "Paciente cadastrado com sucesso"}

    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))

@app.get("/paciente")
def listar_pacientes():
    try:
        lista_pacientes = paciente_service.listar_pacientes()
        return lista_pacientes
        
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))

@app.post("/medico", status_code=201)
def cadastrar_medico(medico:Medico_Create):
    try:
        medico_service.cadastrar_medico(
            nome = medico.nome,
            crm = medico.crm,
            especialidade = medico.especialidade
        )

        return {"message": "Médico cadastrado com sucesso"}

    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))

@app.get("/medico")
def listar_medicos():
    try:
        lista_medicos = medico_service.listar_medicos()
        return lista_medicos

    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
