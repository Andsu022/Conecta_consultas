# Regras de negócio\classe de dados e interação com o banco de dados

from datetime import date
import sqlite3

class Paciente():
    def __init__(self):  # Conexão com o banco de dados
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nascimento TEXT (AAAA-MM-DD) NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT UNIQUE
        )''')
        self.connect.commit()
        self.connect.close()

    def paciente_existente(self, cpf, email):
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute("SELECT cpf, email FROM Pacientes WHERE cpf = ? OR email = ?", (cpf, email))
        result = cursor.fetchone()
        
        if result == None:
            self.connect.close()
            return False
        else:
            self.connect.close()
            return True
 
    def cadastrar_paciente(self, nome, cpf, data_nascimento, telefone, email):
        paciente_existente = self.paciente_existente(cpf,email)
        if paciente_existente:
            raise ValueError("CPF ou email já existentes")
        
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute("""INSERT INTO Pacientes (nome, cpf, data_nascimento, telefone, email) VALUES (?, ?, ?, ?, ?)""", (nome, cpf, data_nascimento, telefone, email))
        self.connect.commit()
        self.connect.close()
        return True

    def listar_pacientes(self):
        self.connect = sqlite3.connect("databank.db")
        self.connect.row_factory = sqlite3.Row
        cursor = self.connect.cursor()
        cursor.execute("SELECT id, nome, cpf, data_nascimento, telefone, email FROM Pacientes")
        pacientes = cursor.fetchall()
        self.connect.close()
        if not pacientes:
            return {"message": "Nenhum paciente cadastrado"}

        return [dict(paciente) for paciente in pacientes]


class Medico():
    def __init__(self):  # Conexão com o banco de dados
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            crm TEXT NOT NULL UNIQUE,
            especialidade TEXT NOT NULL
        )''')
        self.connect.commit()
        self.connect.close()

    def medico_cadastrado(self, crm):
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute("SELECT crm FROM Medicos WHERE crm = ?", (crm,))
        result = cursor.fetchone()
        if result == None:
            self.connect.close()
            return False
        else:
            self.connect.close()
            return True

    def cadastrar_medico(self, nome, crm, especialidade):
        medico_existente = self.medico_cadastrado(crm)
        if medico_existente:
            raise ValueError("Médico já cadastrado")
        
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute("""INSERT INTO Medicos (nome, crm, especialidade) VALUES (?, ?, ?)""", (nome, crm, especialidade))
        self.connect.commit()
        self.connect.close()
        return True

    def listar_medicos(self):
        self.connect = sqlite3.connect("databank.db")
        self.connect.row_factory = sqlite3.Row
        cursor = self.connect.cursor()
        cursor.execute("SELECT id, nome, crm, especialidade FROM Medicos")
        medicos = cursor.fetchall()
        self.connect.close()
        
        if not medicos:
            return {"message": "Nenhum médico cadastrado"}
        
        return [dict(medico) for medico in medicos]

class Consulta():
    def __init__(self):  # Conexão com o banco de dados
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            medico_id INTEGER NOT NULL,
            data_consulta TEXT (AAAA-MM-DD) NOT NULL UNIQUE,
            hora_consulta TEXT (HH:MM) NOT NULL UNIQUE,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
            FOREIGN KEY (medico_id) REFERENCES Medicos(id)
        )''')
        self.connect.commit()
        self.connect.close()

    def agendar_consulta(self, paciente_id, medico_id, data_consulta, hora_consulta):
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM Consultas WHERE medico_id = ? AND data_consulta = ? AND hora_consulta = ?", (medico_id, data_consulta, hora_consulta))
        result = cursor.fetchone()
        if result == None:
            cursor.execute("""INSERT INTO Consultas (paciente_id, medico_id, data_consulta, hora_consulta) VALUES (?, ?, ?, ?)""", (paciente_id, medico_id, data_consulta, hora_consulta))
            self.connect.commit()
            self.connect.close()
            return {"message": "Consulta agendada com sucesso"}
        else:
            self.connect.close()
            return {"message": "Horário indisponível para o médico selecionado"}