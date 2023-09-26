import sqlite3 as sql
from flask import g
from math import floor
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = sql.connect('flask.db')
    return g.link_db
class DataBase:
    def __init__(self, db):
        self.db = db
        self.db.row_factory = sql.Row
        self.cur = db.cursor()

    def create_table(self):
        self.cur.execute("""DROP TABLE posts""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS posts(id INT, 
        title TEXT, 
        text TEXT,
        url TEXT, 
        time INT
        )""")

        self.db.commit()

    def get_posts(self):
        self.cur.execute("""SELECT * FROM posts""")
        return self.cur.fetchall()

    def get_last_post(self):
        self.cur.execute("""
        SELECT * FROM posts WHERE id = (SELECT max(id) FROM posts)
        """)
        return self.cur.fetchone()

    def add_post(self, id, title, text, url, cur_time):
        self.cur.execute("""
        INSERT INTO posts VALUES(?, ?, ?, ?, ?)
        """, (id, title, text, url, floor(cur_time)))
        self.db.commit()

    def get_post(self, id):
        self.cur.execute("""
        SELECT * FROM posts WHERE id = ?
        """, id)
        return self.cur.fetchone()

    def get_post_by_url(self, url):
        self.cur.execute(f"""SELECT * FROM posts WHERE url LIKE '{url}' """)
        return self.cur.fetchone()