import sqlite3
import os


class DBManager:
    def __init__(self):
        os.makedirs("Data", exist_ok=True)
        self.conn = sqlite3.connect("Data/studio.db")
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        # FR-01: Пользователи
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Users 
            (id INTEGER PRIMARY KEY, login TEXT UNIQUE, password TEXT, role TEXT)''')

        # FR-02: Клиенты
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Clients 
            (id INTEGER PRIMARY KEY, fio TEXT, phone TEXT, booking TEXT, rider TEXT)''')

        # FR-03: Договоры
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Contracts 
            (id INTEGER PRIMARY KEY, client_id INTEGER, number TEXT, start_date TEXT, 
             end_date TEXT, amount REAL, status TEXT, FOREIGN KEY(client_id) REFERENCES Clients(id))''')

        # FR-04: Обращения (Заявки)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Requests 
            (id INTEGER PRIMARY KEY, contract_id INTEGER, request_date TEXT, album_type TEXT, 
             status TEXT, title TEXT, artist TEXT, percent REAL, created_at TEXT, updated_at TEXT,
             FOREIGN KEY(contract_id) REFERENCES Contracts(id))''')

        # Тестовый админ
        self.cursor.execute("SELECT * FROM Users WHERE login='admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO Users (login, password, role) VALUES ('admin', 'admin', 'Администратор')")
        self.conn.commit()

    def check_user(self, login, password):
        self.cursor.execute("SELECT role FROM Users WHERE login=? AND password=?", (login, password))
        return self.cursor.fetchone()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def commit_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()