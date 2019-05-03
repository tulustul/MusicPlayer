import math
import logging
from typing import Optional, Any

from core.app import App
from core import config, utils

from .listview import ListComponent
from ..colors import colors

logger = logging.getLogger('ui.table')

FORMATS = {
    'time': utils.format_seconds,
}

def default_format(value):
    return str(value or '')


class TableComponent(ListComponent):

    def __init__(self, **kwargs):
        self._columns = []

        self.headers_color = colors['table-headers']
        self.borders_color = colors['table-borders']
        self.borders_selected_color = colors['table-borders-selected']
        self.header_borders = colors['table-header-borders']
        self.highlighted_color = colors['highlighted-item']
        self.highlighted_selected_color = colors['highlighted-selected-item']

        self.border = config.theme['strings']['border-vertical']

        self.highlighted_item: Optional[Any] = None

        app = App.get_instance()
        app.audio.current_track.subscribe(self.set_highlighed_item)

        super().__init__(**kwargs)

    def set_highlighed_item(self, item: Any):
        self.highlighted_item = item
        self.mark_for_redraw()

    def draw_content(self):
        page_data = self.filtered_data[self.min_index:self.max_index]
        page_data = list(enumerate(page_data))

        self.win.clear()

        x = 0
        for column in self.columns:
            is_last_column = column == self.columns[-1]

            column_size = column['real_size']
            if not is_last_column:
                column_size += len(self.border)

            self.draw_text(
                column['name'], 0, x,
                column_size, self.headers_color,
            )

            if not is_last_column:
                self.win.addstr(
                    0, x + column['real_size'],
                    self.border, self.header_borders,
                )

            formatter = FORMATS.get(column.get('format'), default_format)

            for y, entry in page_data:
                is_selected = entry == self.highlighted_item
                if y + self.min_index == self.index:
                    color = (
                        self.highlighted_selected_color
                        if is_selected else self.selected_color
                    )
                    border_color = self.borders_selected_color
                else:
                    color = (
                        self.highlighted_color if is_selected else self.color
                    )
                    border_color = self.borders_color

                text = formatter(getattr(entry, column['field'], ''))

                # logger.debug('{} {} {}'.format(y, x, text))
                self.draw_text(text, y + 1, x, column['real_size'], color)
                if not is_last_column:
                    self.win.addstr(
                        y + 1, x + column['real_size'],
                        self.border, border_color,
                    )

            x += column['real_size'] + len(self.border)

    @property
    def list_size(self):
        return super().list_size - 1  # minus header

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, columns):
        self._columns = columns
        self.calculate_columns_size()

    def calculate_columns_size(self):
        flex_columns_count = 0
        width = self.rect.width - (len(self.columns) - 1) * len(self.border)

        fixed_columns = [c for c in self.columns if c.get('size')]
        flex_columns = [c for c in self.columns if not c.get('size')]

        for column in fixed_columns:
            column['real_size'] = column['size']

        flex_total_space = width - sum(c['size'] for c in fixed_columns)

        for column in flex_columns:
            column['real_size'] = math.floor(flex_total_space / len(flex_columns))

        if flex_columns:
            total_size = sum(c['real_size'] for c in self.columns)
            flex_columns[0]['real_size'] += width - total_size

    def set_rect(self, *args):
        super().set_rect(*args)
        self.calculate_columns_size()
