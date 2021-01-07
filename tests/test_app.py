import todo_app.app as app

import pytest

import requests

from dotenv import find_dotenv, load_dotenv

from unittest.mock import patch 

import os

from threading import Thread

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

@pytest.fixture
def client():
    # Use out latest integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests
    with test_app.test_client() as client:
        yield client 

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    #Replace call to requests.get(url) with our own function
    mock_get_requests.side_effects = mock_get_cards
    response = client.get('/trello')
    assert response.status_code == 200

def mock_get_cards(url, params):
    if url == f'https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists':
        response = Mock()
        # sample_trello_lists_response should point to some test reponse data
        response.json.return_value = sample_trello_cards_response
        return response
    return None

def create_trello_board():
    board_name = "Tempoary Board"
    params = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN"), "name" : board_name}
    response = requests.post("https://api.trello.com/1/boards/", data = params)
    return response.json()['id']


def delete_trello_board(trello_board_id):
    params = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN")}
    requests.delete("https://api.trello.com/1/boards/" + trello_board_id, data = params)

@pytest.fixture(scope = 'module')
def test_app():
    #Create the new board and update the board id enviroment variable 
    board_id = create_trello_board()
    os.environ['TRELLO BOARD ID'] = board_id

    #construct the new application
    application = app.create_app

    #start the app in its own thread.
    thread = Thread(target =lambda: application.run(use_reloader = False))
    thread.daemon = True
    thread.start()
    yield app

    #Tear Down
    thread.join(1)
    delete_trello_board(board_id)

    
