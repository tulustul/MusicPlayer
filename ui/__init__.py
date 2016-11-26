from .window import Window

win = None


def init():
    global win
    win = Window()


def destroy():
    if win:
        win.destroy()


def initialize():
    win.initialize_view()
