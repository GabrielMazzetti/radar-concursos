import sqlite3
import os

class Database:
    def __init__(self, db_path="database/concursos.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_path)
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orgao TEXT,
                cargo TEXT,
                salario TEXT,
                cidade TEXT,
                inscricao TEXT,
                link TEXT UNIQUE,
                formacoes TEXT,
                texto TEXT,
                data TEXT,
                score INTEGER DEFAULT 0,
                notificado INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def insert_concurso(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO concursos (orgao, cargo, salario, cidade, inscricao, link, formacoes, texto, data, score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('orgao'),
                data.get('cargo'),
                data.get('salario'),
                data.get('cidade'),
                data.get('inscricao'),
                data.get('link'),
                data.get('formacoes'),
                data.get('texto'),
                data.get('data'),
                data.get('score', 0)
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Link already exists
            return False
        finally:
            conn.close()

    def get_unnotified(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM concursos WHERE notificado = 0')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def mark_as_notified(self, contest_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE concursos SET notificado = 1 WHERE id = ?', (contest_id,))
        conn.commit()
        conn.close()
