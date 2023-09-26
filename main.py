from flask import Flask, request, url_for, \
    render_template, flash, get_flashed_messages, \
    session, redirect, abort, g
from config import DATABASE, DEBUG, SECRET_KEY, main_menu
from database import get_db, DataBase
import sqlite3 as sql
import os
import time

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask.db')))
db_path = app.config['DATABASE']

@app.route('/')
def main_page():
    db_temp = get_db()
    db = DataBase(db_temp)
    posts = db.get_posts()
    return render_template('index.html', TITLE='Flask WebApp', menu=main_menu, posts=posts)


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
    db_temp = get_db()
    db = DataBase(db_temp)
    if request.method == 'POST':
        if len(request.form['title']) > 2 and len(request.form['text']) > 10:
            title = request.form['title']
            text = request.form['text']
            url = request.form['url']
            try:
                id = db.get_last_post()['id'] + 1
            except:
                id = 0
            cur_time = time.time()
            db.add_post(id, title, text, url, cur_time)
            flash(message='Thanks for your post!', category='success')
        else:
            flash(message='Invalid format of post', category='error')
    return render_template('add_post.html', TITLE='Add a post', menu=main_menu)


@app.route('/post/<url>')
def post_page(url):
    db_temp = get_db()
    db = DataBase(db_temp)
    try:
        data = db.get_post_by_url(url)
        post_title = data['title']
        post_text = data['text']
        return render_template('post.html',
                               TITLE=f'Post {post_title}',
                               menu=main_menu,
                               post_title=post_title,
                               post_text=post_text)
    except:
        abort(404)


@app.errorhandler(404)
def page404(error):
    return render_template('error_page.html', TITLE=error, menu=main_menu), 404


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()



if __name__ == '__main__':
    print('running')
    app.run(debug=True)

