from .colors import colors
from .listview import List
from errors import errors


class Errors(List):

    HEIGHT = 5

    def __init__(self):
        super().__init__()

        self.normal_color = colors['error']
        self.selected_color = colors['error']

        errors.subscribe(self.add_error)

    def add_error(self, error):
        self.data.append(error)
