# Regras de negócio\classe de dados e interação com o banco de dados
# o retorno dos métodos de cadastro está em inglês para evitar confusão com o nome das classes !
import sqlite3

class Paciente:
    def __init__(self, connection:sqlite3.Connection):
        self.connect = connection
 
    def cadastrar_paciente(self, nome, cpf, data_nascimento, telefone, email):
        try:
            patient = self.connect.execute("""INSERT INTO Pacientes (nome, cpf, data_nascimento, telefone, email) VALUES (?, ?, ?, ?, ?)""", (nome, cpf, data_nascimento, telefone, email))
            self.connect.commit()

        except sqlite3.IntegrityError as e:
            self.connect.rollback()
            message = str(e)

            if "Pacientes.cpf" in message:
                raise ValueError("CPF já cadastrado !")
            if "Pacientes.email" in message:
                raise ValueError("Email já cadastrado !")
            raise

        return patient.lastrowid


    def listar_pacientes(self):

        rows = self.connect.execute("SELECT id, nome, cpf, data_nascimento, telefone, email FROM Pacientes").fetchall()

        return [dict(r) for r in rows]


class Medico():
    def __init__(self, connection:sqlite3.Connection):
        self.connect = connection

    def cadastrar_medico(self, nome, crm, especialidade):
        try:
            doctor = self.connect.execute("""INSERT INTO Medicos (nome, crm, especialidade) VALUES (?, ?, ?)""", (nome, crm, especialidade))
            self.connect.commit()
        except sqlite3.IntegrityError as e:
            self.connect.rollback()
            message = str(e)

            if "Medicos.crm" in message:
                raise ValueError("Médico já cadastrado !")
            raise

        return doctor.lastrowid

    def listar_medicos(self):
        
        rows = self.connect.execute("SELECT id, nome, crm, especialidade FROM Medicos").fetchall()
    
        return [dict(r) for r in rows]
            

class Consulta():
    def __init__(self, connection:sqlite3.Connection):
        self.connect = connection

    def agendar_consulta(self, paciente_id, medico_id, data_consulta, hora_consulta, observacao, situacao):
        try:      
            appointment = self.connect.execute("""INSERT INTO Consultas (paciente_id, medico_id, data_consulta, hora_consulta, observacao, situacao) VALUES (?, ?, ?, ?, ?, ?)""", (paciente_id, medico_id, data_consulta, hora_consulta, observacao, situacao))
            self.connect.commit()
        
        except sqlite3.IntegrityError as e:
            self.connect.rollback()
            message = str(e)

            if "FOREIGN KEY constraint failed" in message:
                raise LookupError("Paciente ou médico informado não existe")
            elif "Consultas.medico_id" in message:
                raise ValueError("Médico já possui consulta nesse horário")
            elif "Consultas.paciente_id" in message:
                raise ValueError("Paciente já possui consulta nesse horário")
            elif "CHECK constraint failed" in message:
                raise ValueError("Situação da consulta inválida")
            raise

        return appointment.lastrowid

    def buscar_consulta(self, id):

        row = self.connect.execute("SELECT id, paciente_id, medico_id, data_consulta, hora_consulta, situacao FROM Consultas WHERE id = ?", (id, )).fetchone()
        if row is None:
            return None

        return dict(row)