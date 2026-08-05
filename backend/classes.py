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