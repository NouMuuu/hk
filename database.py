import sqlite3

def create_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               email TEXT NOT NULL,
               login TEXT NOT NULL,
               password TEXT NOT NULL
               )""")
    conn.commit()
    conn.close()

def add_user(email, login, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (email, login, password)
        VALUES (?, ?, ?)""", (email, login, password))
    
    conn.commit()
    conn.close()

def get_user_by_login(login):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
    user = cursor.fetchone()

    conn.close()
    if user:
        return{
            "id": user[0],
            "email": user[1],
            "login": user[2],
            "password": user[3]
        }
    else:
        return None