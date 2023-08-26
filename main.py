from flask import Flask, request, url_for, \
    render_template, flash, get_flashed_messages, \
    session, redirect, abort
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_sample'
main_menu = [
    {'name': 'Main page', 'url': '/'},
    {'name': 'Downloads', 'url': '/downloads'},
    {'name': 'Contact us', 'url': '/feedback'},
    {'name': 'Sign in', 'url': '/login'}
]
@app.route('/')
def main_page():
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
  
if __name__ == '__main__':
    app.run(debug=True)


