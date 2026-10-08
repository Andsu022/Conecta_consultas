# Regras de negócio\classe de dados e interação com o banco de dados
import sqlite3
from backend.db import get_connection, init_db

class Paciente:
    def __init__(self, connection:sqlite3.Connection):
        self.connect = connection
 
    def cadastrar_paciente(self, nome, cpf, data_nascimento, telefone, email):
        try:
            self.connect.execute("""INSERT INTO Pacientes (nome, cpf, data_nascimento, telefone, email) VALUES (?, ?, ?, ?, ?)""", (nome, cpf, data_nascimento, telefone, email))
            self.connect.commit()

        except sqlite3.IntegrityError as e:
            self.connect.rollback()
            mensage = str(e)

            if "Pacientes.cpf" in mensage:
                raise ValueError("CPF já cadastrado !")
            if "Pacientes.email" in mensage:
                raise ValueError("Email já cadastrado !")
            raise

        return cur

    def listar_paciente(self):

        rows = self.connect.execute("SELECT id, nome, cpf, data_nascimento, telefone, email FROM Pacientes").fetchall()

        return [dict(r) for r in rows]


class Medico():
    def __init__(self, connection:sqlite3.Connection):
        self.connect = connection

    def medico_cadastrado(self, crm):
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT crm FROM Medicos WHERE crm = ?", (crm,))
        result = self.cursor.fetchone()
        
        if result is None:
            return False
        else:
            return True

    def cadastrar_medico(self, nome, crm, especialidade):
        self.cursor = self.connect.cursor()
        medico_existente = self.medico_cadastrado(crm)
        if medico_existente:
            raise ValueError("Médico já cadastrado")
        
        self.cursor.execute("""INSERT INTO Medicos (nome, crm, especialidade) VALUES (?, ?, ?)""", (nome, crm, especialidade))
        self.connect.commit()
        return True

    def listar_medicos(self):
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT id, nome, crm, especialidade FROM Medicos")
        medicos = self.cursor.fetchall()
        
        if not medicos:
            return []
        
        return [dict(medico) for medico in medicos]
            

class Consulta():
    def __init__(self, connection:sqlite3.Connection):
        self.connect = connection

    def consulta_existente(self, medico_id, data_consulta, hora_consulta):
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT medico_id, data_consulta, hora_consulta FROM Consultas WHERE medico_id = ? AND data_consulta = ? AND hora_consulta = ?", (medico_id, data_consulta, hora_consulta))
        result = self.cursor.fetchone()
        
        if result is None:
            return False
        else:
            return True

    def agendar_consulta(self, paciente_id, medico_id, data_consulta, hora_consulta, observacao, situacao):
        self.cursor = self.connect.cursor()
        consulta_existente = self.consulta_existente(medico_id, data_consulta, hora_consulta)
        
        if consulta_existente:
            raise ValueError("Data e horário indisponíveis para o médico selecionado")

        self.cursor.execute("""INSERT INTO Consultas (paciente_id, medico_id, data_consulta, hora_consulta, observacao, situacao) VALUES (?, ?, ?, ?, ?, ?)""", (paciente_id, medico_id, data_consulta, hora_consulta, observacao, situacao))
        self.connect.commit()
        return True

    def listar_consultas(self):
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT id, paciente_id, medico_id, data_consulta, hora_consulta, situacao FROM Consultas")
        consultas = self.cursor.fetchall()
        
        if not consultas:
            return []
        
        return [dict(consulta) for consulta in consultas]