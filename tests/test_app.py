import todo_app.app as app

import pytest

import requests

from dotenv import find_dotenv, load_dotenv

from unittest.mock import patch 

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
    mock_get_requests.side_effects = mock_get_lists
    response = client.get('/trello')

def mock_get_lists(url, params):
    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()
        # sample_trello_lists_response should point to some test reponse data
        response.json.return_value = sample_trello_lists_response
        return response
    return None
    #assert response.status_code == 200