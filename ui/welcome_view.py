from .toolkit.component import Component


class WelcomeView(Component):

    def draw_content(self):
        message = 'This is a very nice welcome message.'[:self.cols]

        y = int((self.cols - len(message)) / 2)
        x = int(self.lines / 2)
        self.win.addstr(x, y, message)
