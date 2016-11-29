import math
import logging

from config import theme
import utils
from .listview import List
from .colors import colors

logger = logging.getLogger('ui')

FORMATS = {
    'time': utils.format_seconds,
}

def default_format(value):
    return str(value or '')


class Table(List):

    def __init__(self):
        self._columns = []

        self.headers_color = colors['table-headers']
        self.borders_color = colors['table-borders']
        self.borders_selected_color = colors['table-borders-selected']
        self.header_borders = colors['table-header-borders']

        self.border = theme['strings']['border-vertical']

        super().__init__()

    def draw_content(self):
        page_data = self.filtered_data[self.min_index:self.max_index]
        page_data = list(enumerate(page_data))

        x = 0
        for column in self.columns:
            is_last_column = column == self.columns[-1]

            column_size = column['real_size']
            if not is_last_column:
                column_size += len(self.border)

            self.draw_text(
                column['name'], x, 0,
                column_size, self.headers_color,
            )

            # if not is_last_column:
            #     self.win.addstr(
            #         0, x + column['real_size'],
            #         self.border, self.header_borders,
            #     )

            formatter = FORMATS.get(column.get('format'), default_format)

            for i, entry in page_data:
                if i + self.min_index == self.index:
                    color = self.selected_color
                    border_color = self.borders_selected_color
                else:
                    color = self.color
                    border_color = self.borders_color

                text = formatter(getattr(entry, column['field'], ''))

                # logger.debug('{} {} {}'.format(x, i + 1, text))
                self.draw_text(text, x, i + 1, column['real_size'], color)
                if not is_last_column:
                    self.win.addstr(
                        i + 1, x + column['real_size'],
                        self.border, border_color,
                    )

            x += column['real_size'] + len(self.border)

        if self.search_enabled:
            self.search_box.refresh()

    # @property
    # def min_index(self):
    #     return max(0, self.page * self.list_size - 1)

    # @property
    # def max_index(self):
        # return (self.page + 1) * self.list_size - 0

    @property
    def list_size(self):
        return super().list_size - 2

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, columns):
        self._columns = columns
        self.calculate_columns_size()

    def calculate_columns_size(self):
        flex_columns_count = 0
        cols = self.cols - (len(self.columns) - 1) * len(self.border)

        fixed_columns = [c for c in self.columns if c.get('size')]
        flex_columns = [c for c in self.columns if not c.get('size')]

        for column in fixed_columns:
            column['real_size'] = column['size']

        flex_total_space = cols - sum(c['size'] for c in fixed_columns)

        for column in flex_columns:
            column['real_size'] = math.floor(flex_total_space / len(flex_columns))

        if flex_columns:
            total_size = sum(c['real_size'] for c in self.columns)
            flex_columns[0]['real_size'] += cols - total_size

    def set_size(self, *args):
        super().set_size(*args)
        self.calculate_columns_size()
