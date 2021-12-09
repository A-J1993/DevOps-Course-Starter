import todo_app.app as app

import pytest

import requests

from dotenv import find_dotenv, load_dotenv

from unittest.mock import patch 

import os

from threading import Thread

import pymongo
from datetime import datetime
from bson.objectid import ObjectId
import mongomock

#Allows one to use json values of null and false in a Python framework
null = None
false = False

sample_trello_lists_response = [
    {
        "id": "5fdcda2428d71e74db64410e",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-12-18T16:34:44.809Z",
        "desc": "",
        "descData": null,
        "dueReminder": null,
        "idBoard": "555555555555555555555555",
        "idList": "333333333333333333333333",
        "idMembersVoted": [],
        "idShort": 12,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Why does this not work",
        "pos": 147456,
        "shortLink": "pLobkTfQ",
        "isTemplate": false,
        "cardRole": null,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": false,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/pLobkTfQ",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/pLobkTfQ/12-why-does-this-not-work",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    }
]

sample_pymongo_card = {"_id": ObjectId("610a77c1aac7db49d161c0f6")
                        ,"name": "card_name"
                        , "status": "To Do"
                        , "dateLastActivity": "2020-12-18T16:34:44.809Z"}

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    #Replace call to requests.get(url) with our own function
    mock_setup_cards()
    response = client.get('/')
    assert response.status_code == 200

def mock_setup_cards():
    mongo_client = pymongo.MongoClient(os.getenv("MONGO_CLIENT"))
    card_board = mongo_client.card_board
    cards = card_board.cards
    post = cards.insert_one(sample_pymongo_card)
