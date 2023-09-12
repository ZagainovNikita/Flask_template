import sqlite3 as sql
from flask import g

def get_db(db_path):
    if not hasattr(g, 'link_db'):
        g.link_db = sql.connect(db_path)
    return g.link_db

sqlScripts = {
    'last_id': 'SELECT * FROM posts WHERE id=(SELECT max(id) FROM posts)',
    'add_post': 'INSERT INTO posts(id, title, text, time) VALUES(?, ?, ?, ?)'
}
def execute_script(db, script, values = None, fetchone = False, fetchall = False):
    cur = db.cursor()
    if values != None:
        cur.execute(script, values)
    else:
        cur.execute(script)
    if fetchone:
        return cur.fetchone()
    if fetchall:
        return cur.fetchall()
    db.commit()