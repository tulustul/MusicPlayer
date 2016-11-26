from rx.subjects import ReplaySubject

from .views import Playlist
from config import config
import context
import stream
import ui

playlist_view = None


def show_playlist(_):
    ui.win.open_view_in(playlist_view, config['playlist']['open_in'])


def init():
    global playlist_view

    stream.register('playlist.tracks', ReplaySubject(1))

    playlist_view = Playlist()
    context.register('playlist')
    context.switch.filter(lambda s: s == 'playlist').subscribe(show_playlist)


def destroy():
    ...
