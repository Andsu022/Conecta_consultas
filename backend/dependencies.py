from backend import classes
from backend.db import get_connection
import sqlite3
from fastapi import Depends


# Dependencias de conexão da requisição
def get_paciente_service(connection: sqlite3.Connection = Depends(get_connection)):
    return classes.Paciente(connection)

def get_medico_service(connection: sqlite3.Connection = Depends(get_connection)):
    return classes.Medico(connection)

def get_consulta_service(connection: sqlite3.Connection = Depends(get_connection)):
    return classes.Consulta(connection)
