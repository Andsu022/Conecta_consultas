import datetime
import sqlite3
class Paciente():
    def __init__(self):
        connect = sqlite3.connect('databank.db')
        cursor = connect.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL
        )''')
        connect.commit()
        connect.close()