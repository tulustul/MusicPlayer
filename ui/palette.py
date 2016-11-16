from .listview import List
from commands import registry


class Palette(List):

    HEIGHT = 5

    def __init__(self):
        super().__init__()

        self._search_enabled = True

        self.data = registry.get_names()

    @property
    def value(self):
        list_value = super().value
        if list_value in self.search_box.text_value:
            return self.search_box.text_value
        else:
            return list_value
