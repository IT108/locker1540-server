import db
import os
from flask import redirect, render_template, url_for, request, Flask, Session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

template_dir = os.path.abspath('html')
template_dir = os.path.join(template_dir, 'templates')
print(template_dir)
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'secretkey'
login_manager = LoginManager(app)
login_manager.login_view = 'auth'


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    error = None
    if request.method == 'POST':
        db_resp = db.check_admin(request.form['username'], request.form['password'])
        if db_resp == 0:
            error = 'Invalid Credentials. Please try again.'
        else:
            user = db.get_user(db_resp)
            login_user(user)

            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/login', methods=['POST'])
def hello_guest():
    return str(db.login(request.values.get('card')))


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
def add_card():
    name = str(request.values.get('name'))
    card = str(request.values.get('card'))
    admin = str(request.values.get('admin'))
    greeting = str(request.values.get('greeting'))
    active = str(request.values.get('active'))
    position = str(request.values.get('position'))
    db.add_user(card, name, admin, greeting, active, position)
    return 'True'


@app.route('/get_all_cards', methods=['POST'])
def get_all_cards():
    return str(db.get_all_users())


@app.route('/delete_card_user', methods=['POST'])
def delete_card_user():
    return str(db.delete_card_user(request.values.get('card')))


@app.route('/delete_name_user', methods=['POST'])
def delete_name_user():
    return str(db.delete_name_user(request.values.get('name')))


@login_manager.user_loader
def load_user(id):
    return db.get_user(id)


if __name__ == '__main__':
    app.run()
