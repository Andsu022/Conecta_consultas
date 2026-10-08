# teste para rodar no banco de dados e verificar se as tabelas foram criadas corretamente

import sqlite3


conn = sqlite3.connect("backend/database/databank.db")
for linha in conn.execute("SELECT type, name, sql FROM sqlite_master"):
    print(linha)

conn.close()

