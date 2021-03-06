"establishes the ToDoCard class"

import os
import requests

import os

from datetime import datetime

class ToDoCard():

    def __init__(self, id, name, status = "To Do", dateLastActivity: datetime = datetime.now()):
        self.id = id
        self.name = name
        self.status = status
        self.dateLastActivity = dateLastActivity

    @classmethod
    def from_trello_card(cls, card):
        status = ""
        dateLastActivity = datetime.strptime(card["dateLastActivity"], '%Y-%m-%dT%H:%M:%S.%fZ')
        if card["idList"] == os.getenv("TRELLO_TODOID"):
            status = "To Do"
        else:
            status = "Done"
        return cls(
            card['id'],
            card['name'],
            status,
            dateLastActivity
            )