import sqlite3 as sql
from flask import g
from config import main_menu

class DataBase:
    def __init__(self, path):
        self.path = path
        self.conn = sql.connect(path)
        self.conn.row_factory = sql.Row
        self.cur = self.conn.cursor()
    def fetchall(self, db_name):
        return self.cur.execute(f"""SELECT * FROM {db_name}""").fetchall()
    def create_db_main_menu(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS main_menu(
            id INT,
            title TEXT,
            url TEXT
            );''')
        self.cur.execute('''DELETE FROM main_menu''')
        for i, item in enumerate(main_menu):
            self.cur.execute(f"""
            INSERT INTO main_menu (id, title, url) VALUES (?, ?, ?)
            """, (i, item['title'], item['url']))
        self.conn.commit()
    def get_main_menu(self):
        return self.cur.execute("""
        SELECT title, url FROM main_menu 
        """).fetchall()
    def get_db(self):
        if not hasattr(g, 'link_db'):
            g.link_db = sql.connect(self.path)
        return g.link_db
