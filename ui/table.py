import logging

from .listview import List

logger = logging.getLogger('ui')


class Table(List):

    def __init__(self):
        super().__init__()
        self.columns = []

    def draw_content(self):
        page_data = self.filtered_data[self.min_index:self.max_index]
        page_data = enumerate(page_data)

        x = 0
        for column in self.columns:
            self.win.addstr(0, x, column['name'], self.selected_color)
            x += int(self.cols / len(self.columns))

        for i, entry in page_data:
            if i + self.min_index == self.index:
                color = self.selected_color
            else:
                color = self.color

            x = 0
            for column in self.columns:
                text = str(getattr(entry, column['field'], ''))
                self.win.addstr(i + 1, x, text, color)
                x += int(self.cols / len(self.columns))

        if self.search_enabled:
            self.search_box.refresh()

    @property
    def max_index(self):
        return (self.page + 1) * self.list_size - 2
