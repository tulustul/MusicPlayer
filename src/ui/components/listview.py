import logging

from .component import Component
from .input import InputComponent
from ..colors import colors

logger = logging.getLogger('ui')


class ListComponent(Component):

    def __init__(self):
        super().__init__()
        self._data = []

        self.filtered_data = []

        self.page = 0

        self.index = 0

        self.search_enabled = False

        # self.search_box = InputComponent()

        # self.search_box.value.subscribe(self.filter_data)

        self.selected_color = colors['selected']

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

        # if self.search_enabled:
        #     self.search_box.refresh()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self.filtered_data = data

    @property
    def search_enabled(self):
        return self._search_enabled

    @search_enabled.setter
    def search_enabled(self, enabled):
        self._search_enabled = enabled
        self.set_size(self.x, self.y, self.cols, self.lines)
        self.mark_for_redraw()

    def set_size(self, x, y, cols, lines):
        # if self.search_enabled:
        #     self.search_box.set_size(x, y, cols, self.search_box.HEIGHT)
        #     y += 1
        #     cols -= 1
        super().set_size(x, y, cols, lines)

    @property
    def min_index(self):
        return max(0, self.page * self.list_size - 1)

    @property
    def max_index(self):
        return (self.page + 1) * self.list_size - 1

    @property
    def value(self):
        return self.filtered_data[self.index]

    @property
    def list_size(self):
        return self.lines

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

    def set_index(self, new_index):
        self.index = max(0, min(new_index, len(self.filtered_data) - 1))
        self.page = int((self.index + 1) / self.list_size)
        self.mark_for_redraw()

    def filter_data(self, term):
        term = term.split()
        if term:
            term = term[0]
            self.filtered_data = [
                entry for entry in self.data if term in entry
            ]
        else:
            self.filtered_data = self.data
        self.mark_for_redraw()

    # def autocomplete_input(self):
    #     logger.warn(self.value)
    #     self.search_box.set_value(self.value)
