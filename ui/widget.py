import curses

from . import colors


class Widget:

    HEIGHT = None

    def __init__(self):
        self.win = None
        self.layout = None

        self.x = 0
        self.y = 0
        self.lines = 0
        self.cols = 0

        self.normal_color = colors.NORMAL
        self.selected_color = colors.SELECTED

    def refresh(self):
        self.win.refresh()

    def set_size(self, x, y, cols, lines):
        self.x = x
        self.y = y
        self.lines = lines
        self.cols = cols
        self.win = curses.newwin(self.lines, self.cols, self.y, 0)
