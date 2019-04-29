import logging

from ui.colors import colors

from .component import Component

logger = logging.getLogger('ui')


class ProgressComponent(Component):

    def __init__(self, **kwargs):
        super().__init__(size=1, **kwargs)

        self.color = colors['bar']
        self.elapsed_color = colors['bar-elapsed']

        self._progress = 0

        self.left_text = ''
        self.right_text = ''

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, progress: float):
        self._progress = progress
        self.mark_for_redraw()

    def set_text(self, left_text: str, right_text=''):
        self.left_text = left_text
        self.right_text = right_text
        self.mark_for_redraw()

    def draw_content(self):
        percantage = int(self.progress * 100)
        right_text = f'{self.right_text} {percantage}'

        max_left_text_length = self.rect.width - len(right_text) - 1
        if len(self.left_text) >= max_left_text_length:
            self.left_text = self.left_text[:max_left_text_length - 2] + '… '

        text = '{}{}{}'.format(
            self.left_text,
            ' ' * (self.rect.width - len(self.left_text) - 1 - len(right_text)),
            right_text,
        )

        progress_div = int(self.rect.width * self.progress)
        progress_div = min(self.rect.width - 1, progress_div)

        self.win.addstr(0, 0, text[:progress_div], self.elapsed_color)
        self.win.addstr(0, progress_div, text[progress_div:], self.color)
        self.win.insch(0, self.rect.width - 1, '%', self.color)
