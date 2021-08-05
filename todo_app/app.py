from flask import Flask, render_template, url_for, redirect, request
from .data.session_items import get_items, add_item
import pymongo
from datetime import datetime
from bson.objectid import ObjectId


#from todo_app.flask_config import Config


import requests

from todo_app.ToDoCard import ToDoCard
from todo_app.ViewModel import ViewModel

import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config')

    @app.route('/hello_world')
    def index():
        items = get_items()
        return render_template('index.html', items = items)

    @app.route('/hello_world', methods = ['POST'])
    def new_item():
        field_name = request.form['field_name']
        add_item(field_name)
        return redirect(url_for('index'))

    @app.route('/')
    def get_cards():
        #params = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN")}
        #cards_in_board = requests.get("https://api.trello.com/1/boards/" + os.getenv("TRELLO_BOARDID") + "/cards", params = params)
        #cards_in_board =  cards_in_board.json()
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client.card_board
        cards = card_board.cards
        #cards = [ToDoCard.from_trello_card(card) for card in cards_in_board]
        all_cards = [ToDoCard.from_mongo_card(card) for card in cards.find()]
        view_model = ViewModel(all_cards)
        return render_template('trello.html', view_model= view_model)

    @app.route('/', methods = ['POST'])
    def add_card():
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client.card_board
        card_name = request.form['field_name']
        cards = card_board.cards
        #params = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN"), "name" : card_name, "idList" : os.getenv("TRELLO_TODOID")}
        #post = requests.post("https://api.trello.com/1/cards/", data = params)
        post = cards.insert_one({"name": card_name, "status": "To Do", "dateLastActivity": datetime.now()})
        return redirect(url_for('get_cards'))


    @app.route('/items/<_id>', methods = ['POST'])
    def complete_card(_id):
        #params = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN"), "idList" : os.getenv("TRELLO_DONEID")}
        #put = requests.put("https://api.trello.com/1/cards/" + id, data=params)
        #mongo_client = pymongo.MongoClient("mongodb+srv://AJ1993:Senkatsam123@cluster0.shd2m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client.card_board
        cards = card_board.cards
        card_to_update = cards.update_one({"_id":ObjectId(_id)}, {"$set" : {"status": "Done", "dateLastActivity": datetime.now()}})
        return redirect(url_for('get_cards'))
    return app
