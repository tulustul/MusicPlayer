from . import colors
from .listview import List
from errors import errors


class Errors(List):

    HEIGHT = 5

    def __init__(self):
        super().__init__()

        self.normal_color = colors.ERROR
        self.selected_color = colors.ERROR

        errors.subscribe(self.add_error)

    def add_error(self, error):
        self.data.append(error)
