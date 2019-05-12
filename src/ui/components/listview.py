import logging
from typing import List, Set, Generic, TypeVar

from rx.subjects import Subject

from core.clipboard import Clipboard

from .component import Component
from ..colors import colors

logger = logging.getLogger('ui')

T = TypeVar('T')


class ListComponent(Generic[T], Component):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data: List[T] = []

        self.filtered_data: List[T] = []

        # Item selected by the user
        self.selected_item = Subject()

        # e.g. currently playing track
        self.distinguished_item: Optional[T] = None

        # Item at "index" position
        self.focused_item = Subject()

        # Items marked in visual mode
        self.marked_items: Set[T] = set()

        self.visual_mode = False

        self.page = 0

        self.index = 0

    def draw_content(self):
        page_data = self.filtered_data[self.min_index:self.max_index]
        page_data = enumerate(page_data)

        self.win.clear()

        for i, item in page_data:
            color = self.get_item_color(item)
            self.win.addstr(i, 0, item, color)

    def get_item_color(self, item: T):
        if self.value == item:
            if item == self.distinguished_item:
                return colors['distinguished-selected-item']
            return colors['selected']

        if item in self.marked_items:
            return colors['marked']

        if item == self.distinguished_item:
            return colors['distinguished-item']

        return colors['normal']

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: List[T]):
        self._data = data
        self.filtered_data = data

    def set_distinguished_item(self, item: T):
        self.distinguished_item = item
        self.mark_for_redraw()

    @property
    def min_index(self):
        return max(0, self.page * self.list_size)

    @property
    def max_index(self):
        return self.min_index + self.list_size

    @property
    def value(self) -> T:
        return self.filtered_data[self.index]

    def get_value(self) -> T:
        return self.filtered_data[self.index]

    @property
    def list_size(self):
        return self.rect.height

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

    def limit_index(self, index: int):
        return max(0, min(index, len(self.filtered_data) - 1))

    def wrap_index(self, index: int):
        if index < 0:
            return len(self.filtered_data) - 1
        if index >= len(self.filtered_data):
            return 0
        return index

    def set_index(self, new_index):
        old_index = self.index
        self.index = self.limit_index(new_index)
        self.page = self.index // self.list_size
        self.focused_item.on_next(self.value)

        if self.visual_mode:
            lower_index = min(old_index, self.index)
            upper_index = max(old_index, self.index)
            items_to_add = set(self.filtered_data[lower_index:upper_index + 1])
            self.marked_items |= items_to_add

        self.mark_for_redraw()

    def select(self):
        self.selected_item.on_next(self.value)
        if hasattr(self, 'on_select'):
            self.on_select(self.value)

    def filter(self, term: str):
        tokens = term.split()
        if tokens:
            self.filtered_data = [
                entry for entry in self.data if tokens[0] in entry
            ]
        else:
            self.filtered_data = self.data[:]
        self.mark_for_redraw()

    def toggle_visual_mode(self):
        self.visual_mode = not self.visual_mode

    def copy_items(self):
        if self.marked_items:
            Clipboard.get_instance().put(self.marked_items)

    def cut_items(self):
        self.copy_items()
        self.delete_items()

    def delete_items(self):
        if hasattr(self, 'on_delete'):
            self.on_delete(self.marked_items or [self.value])
            self.mark_for_redraw()
            self.index = self.limit_index(self.index)

    def paste_items(self):
        if hasattr(self, 'on_paste'):
            self.on_paste(Clipboard.get_instance().get())
            self.mark_for_redraw()
