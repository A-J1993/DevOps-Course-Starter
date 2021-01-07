from selenium import webdriver
import requests
import pytest
import os

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
    application = app.create_app()

    #start the app in its own thread.
    thread = Thread(target =lambda: application.run(use_reloader = False))
    thread.daemon = True
    thread.start()
    yield app

    #Tear Down
    thread.join(1)
    delete_trello_board(board_id)


@pytest.fixture(scope = "module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/trello')
    assert driver.title == 'Trello Cards'
