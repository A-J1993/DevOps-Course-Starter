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

import logging

from loggly.handlers import HTTPSHandler
from logging import Formatter



def writer_required(func):
    @functools.wraps(func)
    def writer_check(*args, **kwargs):
        if os.getenv('LOGIN_DISABLED') != 'True' and current_user.isrole != "writer":
            raise ValueError('Access Denied: Does Not Have Appropiate Privilages')
            #redirect back to page or new page with 403 error?
        else:
            return func(*args, **kwargs)
    return writer_check


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    logger = logging.getLogger(__name__)
    app.logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

    if os.getenv('LOGGLY_TOKEN') is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{os.getenv("LOGGLY_TOKEN")}/tag/todo-app')
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
        app.logger.addHandler(handler)

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        client = WebApplicationClient(os.getenv('CLIENT_ID'))
        github_auth_uri =  client.prepare_request_uri("https://github.com/login/oauth/authorize", redirect_uri=os.getenv("REDIRECT_URI"))
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

    @app.route('/auth_error')
    def auth_error_page():
        return render_template('auth_code_error.html')
    
    @app.route('/user_response_error')
    def user_response_error():
        return render_template('user_response_error.html')

    
    @app.route('/login/callback')
    def verification():
        try:
            auth_code = request.args['code']
        except KeyError:
            app.logger.error("auth_code missing")
            return redirect(url_for('auth_error_page'))
        data = {"code": auth_code, "client_id": os.getenv("CLIENT_ID"), "client_secret": os.getenv("CLIENT_SECRET")}
        #requests.get("https://github.com/login/oauth/authorize", data = data)
        access_token_response = requests.post("https://github.com/login/oauth/access_token", data = data, headers={"Accept": "application/json"})
        client = WebApplicationClient(os.getenv('CLIENT_ID'))
        client.parse_request_body_response(access_token_response.text)
        url, headers, body = client.add_token("https://api.github.com/user")
        user_response = requests.get(url, headers=headers, data=body)
        if not user_response.ok:
            app.logger.error("Problem with getting User info")
            app.logger.error(user_response.text)
            return redirect(url_for('user_response_error.html'))
        user  = User(user_response.json()['id'])
        login_user(user)
        app.logger.info("User " + str(user.id) + " logged in")
        return redirect(url_for('get_cards'))

    
    @app.route('/', methods = ['POST'])
    @writer_required
    def add_card():
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client[os.getenv("DB_NAME")]
        card_name = request.form['field_name']
        cards = card_board.cards
        post = cards.insert_one({"name": card_name, "status": "To Do", "dateLastActivity": datetime.now()})
        app.logger.info("Card ("+ str(card_name) +") Posted")
        return redirect(url_for('get_cards'))

    
    @app.route('/items/<_id>', methods = ['POST'])
    @writer_required
    def complete_card(_id):
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
        card_board = mongo_client[os.getenv("DB_NAME")]
        cards = card_board.cards
        card_to_update = cards.update_one({"_id":ObjectId(_id)}, {"$set" : {"status": "Done", "dateLastActivity": datetime.now()}})
        app.logger.info("Card (" + str(cards.find_one({"_id":ObjectId(_id)}).get("name")) + ") Completed")
        return redirect(url_for('get_cards'))
    
    return app

