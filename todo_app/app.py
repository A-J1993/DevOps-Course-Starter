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
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client[os.getenv("DB_NAME")]
        cards = card_board.cards
        all_cards = [ToDoCard.from_mongo_card(card) for card in cards.find()]
        view_model = ViewModel(all_cards)
        return render_template('cards.html', view_model= view_model)

    @app.route('/', methods = ['POST'])
    def add_card():
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client[os.getenv("DB_NAME")]
        card_name = request.form['field_name']
        cards = card_board.cards
        post = cards.insert_one({"name": card_name, "status": "To Do", "dateLastActivity": datetime.now()})
        return redirect(url_for('get_cards'))


    @app.route('/items/<_id>', methods = ['POST'])
    def complete_card(_id):
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client[os.getenv("DB_NAME")]
        cards = card_board.cards
        card_to_update = cards.update_one({"_id":ObjectId(_id)}, {"$set" : {"status": "Done", "dateLastActivity": datetime.now()}})
        return redirect(url_for('get_cards'))
    return app
