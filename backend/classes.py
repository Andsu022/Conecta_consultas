from datetime import date
import sqlite3

class Paciente():
    def __init__(self):  # Conexão com o banco de dados
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            data_nascimento TEXT (AAAA-MM-DD) NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT
        )''')
        self.connect.commit()
        self.connect.close()

    def cadastrar_paciente(self, nome, cpf, data_nascimento, telefone, email):
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute("SELECT cpf, email FROM Pacientes WHERE cpf = ? AND email = ?", (cpf, email))
        result = cursor.fetchone()
        if result == None:
            cursor.execute("""INSERT INTO Pacientes (nome, cpf, data_nascimento, telefone, email) VALUES (?, ?, ?, ?, ?)""", (nome, cpf, data_nascimento, telefone, email))
            self.connect.commit()
            self.connect.close()
            return "Paciente cadastrado com sucesso"
        else:
            if result[0] == cpf:
                return "CPF já cadastrado"
            else:
                return "Email já cadastrado"

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
            crm TEXT NOT NULL,
            especialidade TEXT NOT NULL,
        )''')
        self.connect.commit()
        self.connect.close()

    def cadastrar_medico(self, nome, crm, especialidade, telefone, email):
        self.connect = sqlite3.connect("databank.db")
        cursor = self.connect.cursor()
        cursor.execute("SELECT crm, email FROM Medicos WHERE crm = ? AND email = ?", (crm, email))
        result = cursor.fetchone()
        if result == None:
            cursor.execute("""INSERT INTO Medicos (nome, crm, especialidade, telefone, email) VALUES (?, ?, ?, ?, ?)""", (nome, crm, especialidade, telefone, email))
            self.connect.commit()
            self.connect.close()
            return "Médico cadastrado com sucesso"
        else:
            if result[0] == crm:
                return "CRM já cadastrado"
            else:
                return "Email já cadastrado"

    def listar_medicos(self):
        self.connect = sqlite3.connect("databank.db")
        self.connect.row_factory = sqlite3.Row
        cursor = self.connect.cursor()
        cursor.execute("SELECT id, nome, crm, especialidade, telefone, email FROM Medicos")
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
            data_consulta TEXT (AAAA-MM-DD) NOT NULL,
            hora_consulta TEXT (HH:MM) NOT NULL,
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
            return "Consulta agendada com sucesso"
        else:
            return "Horário indisponível para o médico selecionado"