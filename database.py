import sqlite3 as sql
from flask import g
def connect_db(path):
    conn = sql.connect(path)
    conn.row_factory = sql.Row
    return conn
def create_db(path):
    db = connect_db(path)
    db.cursor().execute('''CREATE TABLE IF NOT EXISTS data(
    id INT,
    value FLOAT
    );''')
def get_db(path):
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db(path)
    return g.link_db
