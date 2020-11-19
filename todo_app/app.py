from flask import Flask, render_template, url_for, redirect, request
from .data.session_items import get_items, add_item

from todo_app.flask_config import Config
from todo_app.trello_config import KEY, TOKEN, TODOID

import requests

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items = items)

@app.route('/', methods = ['POST'])
def new_item():
    field_name = request.form['field_name']
    add_item(field_name)
    return redirect(url_for('index'))

@app.route('/trello')
def get_cards():
    params = {"key": KEY, "token": TOKEN}
    cards_in_board = requests.get("https://api.trello.com/1/lists/" + TODOID + "/cards", params = params)
    cards_in_board =  cards_in_board.json()
    return render_template('trello.html', items = cards_in_board)

@app.route('/trello', methods = ['POST'])
def add_card():
    card_name = request.form['field_name']
    params = {"key": KEY, "token": TOKEN, "name" : card_name, "idList" : TODOID}
    post = requests.post("https://api.trello.com/1/cards/", data = params)
    return redirect(url_for('get_cards'))
'''
@app.route('trello/<id>', methods = ['PATCH'])
def complete_card():
    params = {"key": KEY, "token": TOKEN, "name" : card_name, "idList" : TODOID}
    return redirect(url_for('get_cards'))
'''

if __name__ == '__main__':
    app.run()
print(KEY)
print(TOKEN)