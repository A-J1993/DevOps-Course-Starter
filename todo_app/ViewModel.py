from datetime import datetime
from datetime import timezone

class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        to_do_items = [x for x in self._items if x.status == "To Do"]
        return to_do_items

    @property
    def done_items(self):
        done_items = [x for x in self._items if x.status == "Done"]
        return done_items

    '''
    def show_all_done_items(self):
        return len(self.done_items) <= 5
    '''

    @property
    def recent_done_items(self):
        done_items = [x for x in self._items if x.status == "Done"]
        recent_done_items = [x for x in done_items if datetime.now().date() == x.dateLastActivity.date()]
        return recent_done_items

    @property
    def older_done_items(self):
        done_items = [x for x in self._items if x.status == "Done"]
        older_done_items = [x for x in done_items if datetime.now().date() != x.dateLastActivity.date()]
        return older_done_items