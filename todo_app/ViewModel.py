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