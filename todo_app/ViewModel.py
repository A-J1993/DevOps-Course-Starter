from datetime import datetime
from datetime import timezone

class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    def to_do_items(self):
        filtered_items = [x for x in self._items if x.status == "To Do"]
        return filtered_items

    def done_items(self):
        filtered_items = [x for x in self._items if x.status == "Done"]
        return filtered_items

    '''
    def show_all_done_items(self):
        return len(self.done_items) <= 5
    '''

    def recent_done_items(self):
        filtered_items = [x for x in self._items if x.status == "Done"]
        filtered_items = [x for x in filtered_items if datetime.now().date() == x.dateLastActivity.date()]
        return filtered_items

    def older_done_items(self):
        filtered_items = [x for x in self._items if x.status == "Done"]
        filtered_items = [x for x in filtered_items if datetime.now().date() != x.dateLastActivity.date()]
        return filtered_items