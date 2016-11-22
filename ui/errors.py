from .listview import List
from errors import errors


class Errors(List):

    HEIGHT = 5

    def __init__(self):
        super().__init__()

        errors.subscribe(self.add_message)

    def add_message(self, message):
        self.data.append(message)
        self.desired_size = len(self.data)
        self.parent.refresh()

    @property
    def visible(self):
        return bool(self.data)

    def draw_content(self):
        for i, entry in enumerate(self.data):
            self.win.addstr(i, 0, entry, self.color)
