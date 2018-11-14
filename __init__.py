import db, constants
import os
from flask import redirect, render_template, url_for, request, Flask, Session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

template_dir = os.path.join(constants.dev_path, 'html')
template_dir = os.path.join(template_dir, 'templates')
print(template_dir)
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'secretkey'
login_manager = LoginManager(app)
login_manager.login_view = 'auth'


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', name = current_user.name[0])


@app.route('/login', methods=['GET','POST'])
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


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/get_all_cards', methods=['POST'])
@login_required
def get_all_cards():
    return str(db.get_all_users())


@app.route('/delete_card_user', methods=['POST'])
@login_required
def delete_card_user():
    return str(db.delete_card_user(request.values.get('card')))


@app.route('/delete_name_user', methods=['POST'])
@login_required
def delete_name_user():
    return str(db.delete_name_user(request.values.get('name')))


@app.route('/sync', methods=['POST'])
@login_required
def sync():
    param = 'id'
    req = request.values.get('sort')
    if req is not None:
        param = req
    return db.sync(param)


@app.route('/open_dialog', methods=['POST'])
@login_required
def open_dialog():
    return db.get_dialog(str(request.values.get('id')))


@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    name = str(request.values.get('name'))
    card = str(request.values.get('card'))
    active = str(request.values.get('active'))
    position = str(request.values.get('position'))
    db.add_user(name, card, active, position)
    return 'OK'


@app.route('/update_user', methods=['POST'])
@login_required
def update_user():
    id = str(request.values.get('id'))
    name = str(request.values.get('name'))
    card = str(request.values.get('card'))
    active = str(request.values.get('active'))
    position = str(request.values.get('position'))
    print(position)
    db.update_user(id, name, card, active, position)
    return 'OK'


@app.route('/toggle_user', methods=['POST'])
@login_required
def toggle_user():
    return db.toggle_user(request.values.get('id'))


@app.route('/add_user_dialog', methods=['POST'])
@login_required
def add_user_dialog():
    error = ''
    if request.values.get('error') is not None:
        error = 'Error:"' + request.values.get('error')
    file = open(constants.server_path + 'html/templates/add_dialog.html')
    return file.read().replace('{{ error }}', error)


@login_manager.user_loader
def load_user(id):
    return db.get_user(id)


if __name__ == '__main__':
    app.run()
