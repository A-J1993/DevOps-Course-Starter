"establishes the ToDoCard class"

import os
import requests

import os

from datetime import datetime

class ToDoCard():

    def __init__(self, _id, name, status = "To Do", dateLastActivity: datetime = datetime.now()):
        self._id = _id
        self.name = name
        self.status = status
        self.dateLastActivity = dateLastActivity

    @classmethod
    def from_mongo_card(cls, card):
        status = "To Do"
        return cls(
            card['_id'],
            card['name'],
            card['status'],
            card["dateLastActivity"]
            )