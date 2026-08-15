# Regras de negócio\classe de dados e interação com o banco de dados

import sqlite3

class ConexaoDatabase:
    def __init__(self):
        self.connect = sqlite3.connect("databank.db")
        self.connect.execute("PRAGMA foreign_keys = ON")
        self.connect.row_factory = sqlite3.Row
        return self.connect

    def close_connection(self):
        self.connect.close()

class Paciente(ConexaoDatabase):
    def __init__(self):  # Conexão com o banco de dados
        super().__init__()
        self.cursor = self.connect.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nascimento TEXT NOT NULL,
            telefone TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        )''')
        self.connect.commit()

    def paciente_existente(self, cpf, email):
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT cpf, email FROM Pacientes WHERE cpf = ? OR email = ?", (cpf, email))
        result = self.cursor.fetchone()
        
        if result is None:
            return False
        else:
            return True
 
    def cadastrar_paciente(self, nome, cpf, data_nascimento, telefone, email):
        self.cursor = self.connect.cursor()
        paciente_existente = self.paciente_existente(cpf,email)
        if paciente_existente:
            raise ValueError("CPF ou email já existentes")
        
        self.cursor.execute("""INSERT INTO Pacientes (nome, cpf, data_nascimento, telefone, email) VALUES (?, ?, ?, ?, ?)""", (nome, cpf, data_nascimento, telefone, email))
        self.connect.commit()

        return True

    def listar_pacientes(self):
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT id, nome, cpf, data_nascimento, telefone, email FROM Pacientes")
        pacientes = self.cursor.fetchall()
        
        if not pacientes:
            raise ValueError("Nenhum paciente cadastrado")

        return [dict(paciente) for paciente in pacientes]


class Medico(ConexaoDatabase):
    def __init__(self):  # Conexão com o banco de dados
        super().__init__()
        self.cursor = self.connect.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            crm TEXT NOT NULL UNIQUE,
            especialidade TEXT NOT NULL
        )''')
        self.connect.commit()

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
            raise ValueError("Nenhum médico cadastrado")
        
        return [dict(medico) for medico in medicos]
            

class Consulta(ConexaoDatabase):
    def __init__(self):  # Conexão com o banco de dados
        super().__init__()
        self.cursor = self.connect.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            medico_id INTEGER NOT NULL,
            data_consulta TEXT NOT NULL,
            hora_consulta TEXT NOT NULL,
            observacao TEXT NOT NULL,
            situacao TEXT NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
            FOREIGN KEY (medico_id) REFERENCES Medicos(id),
            UNIQUE(medico_id, data_consulta, hora_consulta),
            UNIQUE(paciente_id, data_consulta, hora_consulta)
        )''')
        self.connect.commit()

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

        self.cursor.execute("""INSERT INTO Consultas (paciente_id, medico_id, data_consulta, hora_consulta, observacao, situacao) VALUES (?, ?, ?, ?)""", (paciente_id, medico_id, data_consulta, hora_consulta, observacao, situacao))
        self.connect.commit()
        return True

    def listar_consultas(self):
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT id, paciente_id, medico_id, data_consulta, hora_consulta, situacao FROM Consultas")
        consultas = self.cursor.fetchall()
        
        if not consultas:
            raise ValueError("Nenhuma consulta agendada")
        
        return [dict(consulta) for consulta in consultas]