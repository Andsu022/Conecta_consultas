# Arquivo de inicialização do banco de dados SQLite e definição do caminho do arquivo de banco de dados

import sqlite3
from pathlib import Path
from typing import Iterator

DB_PATH = Path(__file__).parent / "database" / "databank.db"


def get_connection() -> Iterator[sqlite3.Connection]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def init_db(connection):
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nascimento TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            crm TEXT NOT NULL UNIQUE,
            especialidade TEXT NOT NULL
        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            medico_id INTEGER NOT NULL,
            data_consulta TEXT NOT NULL,
            hora_consulta TEXT NOT NULL,
            observacao TEXT,
            situacao TEXT NOT NULL default 'agendada'
                CHECK (situacao IN ('agendada', 'realizada', 'cancelada')),
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
            FOREIGN KEY (medico_id) REFERENCES Medicos(id)
        )''')

    cursor.execute('''CREATE UNIQUE INDEX IF NOT EXISTS ux_medico_slot
            ON Consultas(medico_id, data_consulta, hora_consulta)
            WHERE situacao <> 'cancelada' ''')

    cursor.execute('''CREATE UNIQUE INDEX IF NOT EXISTS ux_paciente_slot
            ON Consultas(paciente_id, data_consulta, hora_consulta)
            WHERE situacao <> 'cancelada' ''')
    
    connection.commit()