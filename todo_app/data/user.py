from flask_login import UserMixin
import os

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


    @property
    def isrole(self):
        if self.id == os.getenv('USER_ID'):
            return "writer"
        else:
            return "reader"
        