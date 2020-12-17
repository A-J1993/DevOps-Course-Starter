"establishes the ToDoCard class"

import os
import requests

from todo_app.trello_config import TODOID

class ToDoCard():

    def __init__(self, id, name, status = "To Do"):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card):
        status = ""
        if card["listId"] ==  TODOID:
            status = "To Do"
        else:
            status = "Done"
        return cls(
            card['id'],
            card['name'],
            status
    )