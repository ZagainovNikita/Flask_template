from flask import Flask, request, url_for, \
    render_template, flash, get_flashed_messages, \
    session, redirect, abort, g
from config import main_menu, DATABASE, DEBUG, SECRET_KEY
from database import connect_db, create_db, get_db
import sqlite3 as sql
import os

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask.db')))
db_path = app.config['DATABASE']


@app.route('/')
def main_page():
    db_temp = get_db(db_path)
    return render_template('index.html', TITLE = 'Flask WebApp', menu = main_menu)

@app.route('/feedback', methods = ['POST', 'GET'])
def contact_page():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            print(request.form)
            flash('Thanks for your message!', category='success')
        else:
            flash('Invalid login', category='error')
    return render_template('feedback.html', TITLE = 'Contact us', menu = main_menu)

@app.route('/login', methods = ['POST', 'GET'])
def login_page():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST':
        if request.form['username'] == 'Nikita' and request.form['password'] == 'A120':
            session['userLogged'] = request.form['username']
            return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', TITLE = 'Sign in', menu = main_menu)

@app.route('/profile/<username>')
def profile(username):
    if session.get('userLogged') != username:
        abort(401)
    return f'profile page of {username}'

@app.errorhandler(404)
def page404(error):
    return render_template('error_page.html', TITLE=error, menu=main_menu), 404

@app.teardown_appcontext
def closr_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True)

