import logging

import curses

logger = logging.getLogger(name='ui')


class Layout:

    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.widgets = []

    def add(self, new_widget):
        new_widget.layout = self
        self.widgets.append(new_widget)
        self.refresh()

    def remove(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
            self.refresh()

    def refresh(self):
        self.parent_screen.clear()
        self.parent_screen.refresh()
        self.update_sizes()
        for widget in self.widgets:
            widget.refresh()

    def update_sizes(self):
        y = 0

        fluent_widget_height = curses.LINES - sum(
            widget.HEIGHT for widget in self.widgets if widget.HEIGHT
        )

        logger.warn(self.widgets)
        for widget in self.widgets:
            height = widget.HEIGHT or fluent_widget_height
            widget.set_size(0, y, curses.COLS, height)
            logger.warn('update sizes {} {}'.format(widget, height))
            y += height
