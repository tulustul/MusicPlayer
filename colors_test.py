import curses


def main(stdscr):
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, 0, i)
        stdscr.addstr(' {} '.format(i), curses.color_pair(i))
    stdscr.getch()


curses.wrapper(main)
