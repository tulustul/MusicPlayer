import os
import logging
import threading

from gi.repository import AppIndicator3
from gi.repository import Gtk

import commands
from plugins.track_scheduler import commands as track_scheduler_commands

logger = logging.getLogger('tray-menu')


def pause(data=None):
    commands.pause_track()


def play(data=None):
    commands.play_track()


def next_track(data=None):
    track_scheduler_commands.next_track()


def random_track(data=None):
    track_scheduler_commands.random_track()


def quit_app(data=None):
    Gtk.main_quit()
    commands.quit()


def make_menu():
    menu = Gtk.Menu()

    pause_item = Gtk.MenuItem('Pause')
    play_item = Gtk.MenuItem('Play')
    next_item = Gtk.MenuItem('Next')
    random_item = Gtk.MenuItem('Random')
    quit_item = Gtk.MenuItem('Quit')

    # Append the menu items
    menu.append(pause_item)
    menu.append(play_item)
    menu.append(next_item)
    menu.append(random_item)
    menu.append(quit_item)

    # add callbacks
    pause_item.connect_object('activate', pause, 'pause_item')
    play_item.connect_object('activate', play, 'play_item')
    next_item.connect_object('activate', next_track, 'next_item')
    random_item.connect_object('activate', random_track, 'random_item')
    quit_item.connect_object('activate', quit_app, 'quit_item')

    # Show the menu items
    menu.show_all()

    return menu


def run_gtk_loop():
    try:
        icon = os.path.abspath('plugins/tray-menu/tray-icon.png')
        ind = AppIndicator3.Indicator.new(
            'music', icon, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES,
        )
        ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        menu = make_menu()

        ind.set_menu(menu)
        Gtk.main()
    except Exception as e:
        logger.error(str(e))


def init():
    t = threading.Thread(target=run_gtk_loop)
    t.daemon = True
    t.start()
