from flask import Flask, render_template, url_for, redirect, request
from .data.session_items import get_items, add_item

from todo_app.flask_config import Config
from todo_app.trello_config import KEY, TOKEN, TODOID, DONEID

import requests

from todo_app.ToDoCard import ToDoCard
from todo_app.ViewModel import ViewModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

'''class ToDoCard():

    def __init__(self, id, name):
        self.id = id
        self.name = name

class ViewModel:
    def __init__(self, items):
            self._items = items
    
    @property
    def items(self):
        return self._items
'''

app = create_app()

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
    to_do_cards_in_list = requests.get("https://api.trello.com/1/lists/" + TODOID + "/cards", params = params)
    to_do_cards_in_list =  to_do_cards_in_list.json()
    to_do_cards = [ToDoCard.from_trello_card(card) for card in to_do_cards_in_list]
    view_model_to_do = ViewModel(to_do_cards).to_do_items


    done_cards_in_list = requests.get("https://api.trello.com/1/lists/" + DONEID + "/cards", params = params)
    done_cards_in_list =  done_cards_in_list.json()
    done_cards = [ToDoCard.from_trello_card(card) for card in done_cards_in_list]

    view_model_done = ViewModel(done_cards).done_items
    return render_template('trello.html', view_model_to_do = view_model_to_do, view_model_done = view_model_done)

@app.route('/trello', methods = ['POST'])
def add_card():
    card_name = request.form['field_name']
    params = {"key": KEY, "token": TOKEN, "name" : card_name, "idList" : TODOID}
    post = requests.post("https://api.trello.com/1/cards/", data = params)
    return redirect(url_for('get_cards'))


@app.route('/trello/<id>', methods = ['POST'])
def complete_card(id):
    params = {"key": KEY, "token": TOKEN, "idList" : DONEID}
    put = requests.put("https://api.trello.com/1/cards/" + id, data=params)
    return redirect(url_for('get_cards'))

if __name__ == '__main__':
    app.run()
print(KEY)
print(TOKEN)


