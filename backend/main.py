# Criação de rotas e API REST no FastAPI
import classes
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

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
    telefone: str
    email: str

class Consulta_Create(BaseModel):
    paciente_id: int
    medico_id: int
    data_consulta: str
    hora_consulta: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#app.mount("/static", StaticFiles(directory="static"), name="static")

paciente_service = classes.Paciente()
medico_service = classes.Medico()
consulta_service = classes.Consulta()

@app.post("/paciente")
def cadastrar_paciente(paciente:Paciente_Create):
    resultado = paciente_service.cadastrar_paciente(
        nome = paciente.nome,
        cpf = paciente.cpf,
        data_nascimento = paciente.data_nascimento,
        telefone = paciente.telefone,
        email = paciente.email
    )
    message = resultado.get("message", "")
    if "Paciente cadastrado com sucesso" in message:
        return resultado
    if "CPF já cadastrado" in message:
        raise HTTPException(status_code=400, detail=resultado)
    if "Email já cadastrado" in message:
        raise HTTPException(status_code=400, detail=resultado)

@app.get("/paciente")
def listar_pacientes():
    resultado = paciente_service.listar_pacientes()
    if isinstance(resultado, dict) and "Nenhum paciente cadastrado" in resultado.get("message", ""):
        raise HTTPException(status_code=404, detail=resultado)
    else:
        return resultado

@app.post("/medico")
def cadastrar_medico(medico:Medico_Create):
    resultado = medico_service.cadastrar_medico(
        nome = medico.nome,
        crm = medico.crm,
        especialidade = medico.especialidade,
        telefone = medico.telefone,
        email = medico.email
    )
    if "Médico cadastrado com sucesso" in resultado:
        return
    if "CRM já cadastrado" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    if "Email já cadastrado" in resultado:
        raise HTTPException(status_code=400, detail=resultado)