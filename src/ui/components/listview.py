import logging

from rx.subjects import Subject

from .component import Component
from ..colors import colors

logger = logging.getLogger('ui')


class ListComponent(Component):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = []

        self.filtered_data = []

        self.page = 0

        self.index = 0

        self.selected_color = colors['selected']

        self.selected_item = Subject()

        self.highlighted_item = Subject()

    def draw_content(self):
        page_data = self.filtered_data[self.min_index:self.max_index]
        page_data = enumerate(page_data)

        self.win.clear()

        for i, entry in page_data:
            if i + self.min_index == self.index:
                color = self.selected_color
            else:
                color = self.color

            self.win.addstr(i, 0, entry, color)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self.filtered_data = data

    @property
    def min_index(self):
        return max(0, self.page * self.list_size)

    @property
    def max_index(self):
        return self.min_index + self.list_size

    @property
    def value(self):
        return self.filtered_data[self.index]

    @property
    def list_size(self):
        return self.rect.height

    @property
    def highlighted_item_index(self):
        return self.filtered_data.index(self.highlighted_item)

    def go_by(self, offset):
        self.set_index(self.index + offset)

    def go_top(self):
        self.set_index(0)

    def go_bottom(self):
        self.set_index(len(self.filtered_data) - 1)

    def next_page(self):
        self.set_index(self.index + self.list_size)

    def previous_page(self):
        self.set_index(self.index - self.list_size)

    def limit_index(self, current_index: int, new_index: int):
        return max(0, min(new_index, len(self.filtered_data) - 1))

    def wrap_index(self, index: int):
        if index < 0:
            return len(self.filtered_data) - 1
        if index >= len(self.filtered_data):
            return 0
        return index

    def set_index(self, new_index):
        self.index = self.limit_index(self.index, new_index)
        self.page = self.index // self.list_size
        self.highlighted_item.on_next(self.value)
        self.mark_for_redraw()

    def select(self):
        self.selected_item.on_next(self.value)

    def filter(self, term: str):
        tokens = term.split()
        if tokens:
            self.filtered_data = [
                entry for entry in self.data if tokens[0] in entry
            ]
        else:
            self.filtered_data = self.data[:]
        self.mark_for_redraw()
