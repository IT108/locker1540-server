import db
import os
from flask import redirect, render_template, url_for, request, Flask

template_dir = os.path.abspath('html')
template_dir = os.path.join(template_dir, 'templates')
print(template_dir)
app = Flask(__name__, template_folder=template_dir)


@app.route('/index')
def index():
    return 'Hello!'


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    error = None
    if request.method == 'POST':
        print(request.get_data())
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return 'Logged in'
    return render_template('login.html', error=error)


@app.route('/login', methods=['POST'])
def hello_guest():
    return str(db.login(request.values.get('card')))


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


if __name__ == '__main__':
    app.run()
