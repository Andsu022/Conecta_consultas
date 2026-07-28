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
        cursor.execute("SELECT cpf FROM Pacientes WHERE cpf = ?", (cpf,))
        if cursor.fetchone() == None:
            cursor.execute("""INSERT INTO Pacientes (nome, cpf, data_nascimento, telefone, email) VALUES (?, ?, ?, ?, ?)""", (nome, cpf, data_nascimento, telefone, email))
            self.connect.commit()
            self.connect.close()
            return "Paciente cadastrado com sucesso"
        else:
            return "CPF já cadastrado"

        
    