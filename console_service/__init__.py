import os

from flask import redirect, render_template, url_for, request, Flask
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.urls import url_parse

import constants as constants
import pre_start
from backend.db import auth
from backend.pages import users, admins

app = Flask(__name__)
login_manager = LoginManager(app)
app, login_manager = pre_start.run(app, login_manager)


@app.before_request
def before_request():
    constants.DB.connect()


@app.after_request
def after_request(response):
    constants.DB.close()
    return response


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if current_user.is_authenticated:
        return redirect(url_for('index_route'))
    error = None
    if request.method == 'POST':
        db_resp = auth.check_admin(request.form['username'], request.form['password'])
        if db_resp == 0:
            error = 'Invalid Credentials. Please try again.'
        else:
            user = auth.get_user(db_resp)
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index_route')
            return redirect(next_page)
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET'])
@login_required
def logout_route():
    logout_user()
    return redirect(url_for('index_route'))


# <------------------------------------------------USERS------------------------------------------------>


@app.route('/')
@app.route('/users')
@login_required
def index_route():
    return render_template('users.html', name=current_user.name[0])


@app.route('/sync', methods=['POST'])
@login_required
def sync_route():
    param = 'id'
    req = request.values.get('sort')
    if req is not None:
        param = req
    return users.sync(param)


@app.route('/add_user', methods=['POST'])
@login_required
def add_user_route():
    name = str(request.values.get('name'))
    card = str(request.values.get('card'))
    active = str(request.values.get('active'))
    position = str(request.values.get('position'))
    users.add_user(name, card, active, position)
    return 'OK'


@app.route('/update_user', methods=['POST'])
@login_required
def update_user_route():
    id = str(request.values.get('id'))
    name = str(request.values.get('name'))
    card = str(request.values.get('card'))
    active = str(request.values.get('active'))
    position = str(request.values.get('position'))
    print(position)
    users.update_data(id, name, card, active, position)
    return 'OK'


@app.route('/toggle_user', methods=['POST'])
@login_required
def toggle_user_route():
    return users.toggle_user(request.values.get('id'))


@app.route('/open_dialog', methods=['POST'])
@login_required
def open_dialog_route():
    return users.get_dialog(str(request.values.get('id')))


@app.route('/add_user_dialog', methods=['POST'])
@login_required
def add_user_dialog_route():
    error = ''
    if request.values.get('error') is not None:
        error = 'Error:"' + request.values.get('error')
    file = open(os.path.join(constants.current_path, 'html/templates/users/add_dialog.html'))
    return file.read().replace('{{ error }}', error)


# <------------------------------------------------ADMINS------------------------------------------------>


@app.route('/admins', methods=['GET'])
@login_required
def admins_route():
    return render_template('admins.html', name=current_user.name[0])


@app.route('/sync_admins', methods=['POST'])
@login_required
def sync_admins_route():
    param = 'id'
    req = request.values.get('sort')
    if req is not None:
        param = req
    return admins.sync(param)


@app.route('/toggle_admin', methods=['POST'])
@login_required
def toggle_admin_route():
    return admins.toggle_user(request.values.get('id'))


@app.route('/add_admin', methods=['POST'])
@login_required
def add_admin_route():
    name = str(request.values.get('name'))
    email = str(request.values.get('email'))
    login = str(request.values.get('login'))
    password = str(request.values.get('password'))
    return admins.add_user(name, email, login, password)


@app.route('/update_admin', methods=['POST'])
@login_required
def update_admin_route():
    id = str(request.values.get('id'))
    name = str(request.values.get('name'))
    email = str(request.values.get('email'))
    login = str(request.values.get('login'))
    return admins.update_admin(id, name, email, login)


@app.route('/delete_admin', methods=['POST'])
@login_required
def delete_admin_route():
    id = str(request.values.get('id'))
    admins.delete_admin(id)
    return 'OK'


@app.route('/open_admin_dialog', methods=['POST'])
@login_required
def open_admin_dialog_route():
    return admins.get_dialog(str(request.values.get('id')))


@app.route('/add_admin_dialog', methods=['POST'])
@login_required
def add_admin_dialog_route():
    return admins.get_empty_dialog()


@login_manager.user_loader
def load_user(id):
    return auth.get_user(id)


if __name__ == '__main__':
    app.run()
