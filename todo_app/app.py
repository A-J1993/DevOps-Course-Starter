from flask import Flask, render_template, url_for, redirect, request
from flask_login.utils import login_user
from werkzeug.datastructures import Accept

from todo_app.data.user import User
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from flask_login import LoginManager, login_required, current_user
from oauthlib.oauth2 import WebApplicationClient

from todo_app.flask_config import Config


import requests
import os
import functools


from todo_app.ToDoCard import ToDoCard
from todo_app.ViewModel import ViewModel

import os


def writer_required(func):
    @functools.wraps(func)
    def writer_check():
        if current_user.user_id != os.getenv("USER_ID"):
            raise ValueError('Access Denied: Does Not Have Appropiate Privilages')
            #redirect back to page or new page with 403 error?
        else:
            func()
    return writer_check


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        client = WebApplicationClient(os.getenv('CLIENT_ID'))
        github_auth_uri =  client.prepare_request_uri("https://github.com/login/oauth/authorize", redirect_uri="http://127.0.0.1:5000/login/callback")
        return redirect(github_auth_uri)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)
    
    login_manager.init_app(app)


    @app.route('/')
    @login_required
    def get_cards():
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client[os.getenv("DB_NAME")]
        cards = card_board.cards
        all_cards = [ToDoCard.from_mongo_card(card) for card in cards.find()]
        view_model = ViewModel(all_cards)
        return render_template('cards.html', view_model= view_model)
    
    @app.route('/login/callback')
    def something():
        auth_code = request.args['code']
        data = {"code": auth_code, "client_id": os.getenv("CLIENT_ID"), "client_secret": os.getenv("CLIENT_SECRET")}
        #requests.get("https://github.com/login/oauth/authorize", data = data)
        access_token_response = requests.post("https://github.com/login/oauth/access_token", data = data, headers={"Accept": "application/json"})
        client = WebApplicationClient(os.getenv('CLIENT_ID'))
        client.parse_request_body_response(access_token_response.text)
        url, headers, body = client.add_token("https://api.github.com/user")
        user_response = requests.get(url, headers=headers, data=body)
        user  = User(user_response.json()['id'])
        login_user(user)
        print("User ID is: " + str(user.id))
        return redirect(url_for('get_cards'))

    
    @writer_required
    @app.route('/', methods = ['POST'])
    def add_card():
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client[os.getenv("DB_NAME")]
        card_name = request.form['field_name']
        cards = card_board.cards
        post = cards.insert_one({"name": card_name, "status": "To Do", "dateLastActivity": datetime.now()})
        return redirect(url_for('get_cards'))

    @writer_required
    @app.route('/items/<_id>', methods = ['POST'])
    def complete_card(_id):
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client[os.getenv("DB_NAME")]
        cards = card_board.cards
        card_to_update = cards.update_one({"_id":ObjectId(_id)}, {"$set" : {"status": "Done", "dateLastActivity": datetime.now()}})
        return redirect(url_for('get_cards'))
    

    return app

