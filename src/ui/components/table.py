import math
import logging
from typing import Generic, TypeVar

from core import config, utils

from .listview import ListComponent
from ..colors import colors

logger = logging.getLogger("ui.table")

FORMATS = {"time": utils.format_seconds}


def default_format(value):
    return str(value or "")


T = TypeVar("T")


class TableComponent(Generic[T], ListComponent[T]):
    def __init__(self, **kwargs):
        self._columns = []

        self.border = config.theme["strings"]["border-vertical"]

        super().__init__(**kwargs)

    def draw_content(self):
        page_data = self.filtered_data[self.min_index : self.max_index]
        page_data = list(enumerate(page_data))

        self.win.clear()

        x = 0
        for column in self.columns:
            is_last_column = column == self.columns[-1]

            column_size = column["real_size"]
            if not is_last_column:
                column_size += len(self.border)

            self.draw_text(
                column["name"], 0, x, column_size, colors["headers"]
            )

            formatter = FORMATS.get(column.get("format"), default_format)

            for y, item in page_data:
                color = self.get_item_color(item)

                text = formatter(getattr(item, column["field"], ""))

                self.draw_text(text, y + 1, x, column["real_size"], color)
                if not is_last_column:
                    self.win.addstr(
                        y + 1, x + column["real_size"], self.border, color
                    )

            x += column["real_size"] + len(self.border)

    def get_item_color(self, item: T):
        if self.value == item:
            if item == self.distinguished_item:
                return colors["distinguished-selected-item"]
            return colors["selected"]

        if item in self.marked_items:
            return colors["marked"]

        if item == self.distinguished_item:
            return colors["distinguished-item"]

        return colors["normal"]

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
        width = self.rect.width - (len(self.columns) - 1) * len(self.border)

        fixed_columns = [c for c in self.columns if c.get("size")]
        flex_columns = [c for c in self.columns if not c.get("size")]

        for column in fixed_columns:
            column["real_size"] = column["size"]

        flex_total_space = width - sum(c["size"] for c in fixed_columns)

        for column in flex_columns:
            column["real_size"] = math.floor(
                flex_total_space / len(flex_columns)
            )

        if flex_columns:
            total_size = sum(c["real_size"] for c in self.columns)
            flex_columns[0]["real_size"] += width - total_size

    def set_rect(self, *args):
        super().set_rect(*args)
        self.calculate_columns_size()
