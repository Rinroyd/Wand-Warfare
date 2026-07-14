import sqlite3
import os
from datetime import date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.db")

class LeaderboardDB:

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                score INTEGER NOT NULL,
                level INTEGER NOT NULL DEFAULT 1,
                date_achieved TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def add_score(self, username, score, level=1, date_achieved=None):
        if not username:
            username = "Player"
        if date_achieved is None:
            date_achieved = date.today().isoformat()

        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO scores (username, score, level, date_achieved) VALUES (?, ?, ?, ?)",
            (username, score, level, date_achieved),
        )
        conn.commit()
        conn.close()

    def get_top_scores(self, limit=10):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT username, score, level, date_achieved FROM scores ORDER BY score DESC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
        conn.close()
        return rows

    def search_player(self, username, limit=10):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT username, score, level, date_achieved FROM scores "
            "WHERE username LIKE ? ORDER BY score DESC LIMIT ?",
            (f"%{username}%", limit),
        )
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_rank(self, username):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT username FROM scores ORDER BY score DESC")
        rows = [r[0] for r in cur.fetchall()]
        conn.close()
        for i, uname in enumerate(rows):
            if uname.lower() == username.lower():
                return i + 1
        return None
