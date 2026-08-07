import classes
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/static", StaticFiles(directory="static"), name="static")

paciente = classes.Paciente()
medico = classes.Medico()
consulta = classes.Consulta()

app.add_api_route("/cadastrar_paciente", paciente.cadastrar_paciente, methods=["POST"])
app.add_api_route("/listar_pacientes", paciente.listar_pacientes, methods=["GET"])


