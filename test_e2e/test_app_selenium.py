from selenium import webdriver
import requests
import pytest
import os
import todo_app.app as app
from dotenv import find_dotenv, load_dotenv
from threading import Thread

@pytest.fixture
def client():
    # Use out latest integration config instead of the 'real' version
    file_path = find_dotenv('.env')
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

    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

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
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'Trello Cards'

def test_add_card(driver, test_app):
    driver.get('http://localhost:5000/')
    link = driver.find_element_by_id('Submit Card')
    link.click()
    assert driver.find_element_by_class_name("Card-Class")