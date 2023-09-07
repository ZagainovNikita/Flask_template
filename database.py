import sqlite3 as sql
class DB:
    def __init__(self, path):
        self.conn = sql.connect(path)
        self.conn.row_factory = sql.Row
        self.path = path
        self.cur = self.conn.cursor()
