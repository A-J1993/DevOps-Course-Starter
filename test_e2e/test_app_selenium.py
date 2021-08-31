from selenium import webdriver
import requests
import pytest
import os
import todo_app.app as app
from dotenv import find_dotenv, load_dotenv
from threading import Thread
from pymongo import MongoClient 
import datetime

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



def create_database(client, database_name):
    #database_name = "Temporary_Database"
    db = client[database_name]
    temp_collection = db.temp_collection
    post = temp_collection.insert_one({"name": "test", "status": "To Do", "dateLastActivity": datetime.datetime.now()})
    assert database_name in client.list_database_names()

def delete_database(client, database_name):
    client.drop_database(database_name)
    assert database_name not in client.list_database_names()

@pytest.fixture(scope = 'module')
def test_app():
    #Create the new board and update the board id enviroment variable 

    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    mongo_client = MongoClient(os.getenv("MONGO_CLIENT"))

    database_name = "Temporary_Database"
    create_database(mongo_client, database_name)
    
    #construct the new application
    application = app.create_app()

    #start the app in its own thread.
    thread = Thread(target =lambda: application.run(use_reloader = False))
    thread.daemon = True
    thread.start()
    yield app

    #Tear Down
    thread.join(1)
    delete_database(mongo_client, database_name)


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