from flask import Flask, request, url_for, \
    render_template, flash, get_flashed_messages, \
    session, redirect, abort, g
from config import DATABASE, DEBUG, SECRET_KEY, main_menu
from database import get_db, sqlScripts, execute_script
import sqlite3 as sql
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask.db')))
db_path = app.config['DATABASE']

@app.route('/')
def main_page():
    return render_template('index.html', TITLE='Flask WebApp', menu=main_menu)

@app.route('/feedback', methods = ['POST', 'GET'])
def contact_page():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            print(request.form)
            flash('Thanks for your message!', category='success')
        else:
            flash('Invalid login', category='error')
    return render_template('feedback.html', TITLE='Contact us', menu=main_menu)

@app.route('/login', methods = ['POST', 'GET'])
def login_page():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST':
        if request.form['username'] == 'Nikita' and request.form['password'] == 'A120':
            session['userLogged'] = request.form['username']
            return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', TITLE='Sign in', menu=main_menu)

@app.route('/profile/<username>')
def profile(username):
    if session.get('userLogged') != username:
        abort(401)
    return f'profile page of {username}'

@app.route('/add_post', methods = ['GET', 'POST'])
def add_post():
    db_temp = get_db(db_path)
    if request.method == 'POST':
        if len(request.form['title']) > 2 and len(request.form['text']) > 10:
            title = request.form['title']
            text = request.form['text']
            try:
                id = execute_script(db_temp, sqlScripts['last_id'], fetchone=True)['id'] + 1
            except:
                id = 0
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            execute_script(db_temp, sqlScripts['add_post'], (id, title, text, time))
            flash(message='Thanks for your post!', category='success')
        else:
            flash(message='Invalid format of post', category='error')
    return render_template('add_post.html', TITLE='Add a post', menu=main_menu)

@app.errorhandler(404)
def page404(error):
    return render_template('error_page.html', TITLE=error, menu=main_menu), 404

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True)

