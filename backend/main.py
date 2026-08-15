# Criação de rotas e API REST no FastAPI
import classes
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date, time

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
    observacao: str
    situacao: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"]
)

@app.post("/paciente", status_code=201)
def cadastrar_paciente(paciente:PacienteCreate):
    paciente_service = classes.Paciente()
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
    finally:
        paciente_service.close_connection()

@app.get("/paciente")
def listar_pacientes():
    paciente_service = classes.Paciente()
    try:
        lista_pacientes = paciente_service.listar_pacientes()
        return lista_pacientes
        
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    finally:
        paciente_service.close_connection()

@app.post("/medico", status_code=201)
def cadastrar_medico(medico:MedicoCreate):
    medico_service = classes.Medico()
    try:
        medico_service.cadastrar_medico(
            nome = medico.nome,
            crm = medico.crm,
            especialidade = medico.especialidade
        )

        return {"message": "Médico cadastrado com sucesso"}

    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))
    finally:
        medico_service.close_connection()

@app.get("/medico")
def listar_medicos():
    medico_service = classes.Medico()
    try:
        lista_medicos = medico_service.listar_medicos()
        return lista_medicos

    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    finally:
        medico_service.close_connection()
