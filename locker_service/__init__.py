from flask import Flask
from flask import request
import db, constants
app = Flask(__name__)

@app.route('/card', methods=['POST'])
def hello_guest():
    return str(db.get_card(request.values.get('card')))


@app.route('/greet', methods=['POST'])
def get_greet():
    return str(db.get_greet(request.values.get('card')))


@app.route('/sync', methods=['POST'])
def sync():
    return str(db.sync())


if __name__ == '__main__':
    app.run()
