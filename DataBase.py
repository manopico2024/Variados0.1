import sqlite3

def conexao_db():  
    conn = sqlite3.connect('DataBase.db')
    cursor = conn.cursor()
    
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Local TEXT NOT NULL,
        Valor TEXT NOT NULL,
        Pago TEXT NOT NULL,
        Serie TEXT NOT NULL,
        Data TEXT NOT NULL,
        Data2 TEXT NOT NULL,
        Data3 TEXT NOT NULL,
        Recebido TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
