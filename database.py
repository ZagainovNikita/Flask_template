import sqlite3 as sql
from flask import g
from config import main_menu
from datetime import datetime
class DataBase:
    def __init__(self, conn):
        self.conn = conn
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


    def create_db_posts(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS posts(
        id INT,
        title TEXT,
        text TEXT,
        time TEXT
        );''')
        self.conn.commit()


    def add_post(self, title, text):
        last_post = self.cur.execute('''
        SELECT * FROM posts WHERE id=(SELECT max(id) FROM posts)
        ''')
        id = last_post['id'] + 1
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        self.cur.execute("""
        INSERT INTO posts(id, title, text, time) VALUES(?, ?, ?, ?)
        """, (id, title, text, time))
        self.conn.commit()
    def get_db(self):
        if not hasattr(g, 'link_db'):
            g.link_db = sql.connect(self.path)
        return g.link_db
