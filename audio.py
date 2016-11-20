import asyncio
import logging
import threading

logger = logging.getLogger('audio')

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject
from gi.repository import Gst

from config import config
from errors import errors
import playback

playbin = None
pipeline = None
bus = None
loop = None
playing = False


def init(loop_):
    global playbin
    global pipeline
    global bus
    global loop

    loop = loop_

    GObject.threads_init()
    Gst.init(None)

    pipeline = Gst.Pipeline('mypipeline')

    playbin = Gst.ElementFactory.make('playbin', None)
    if not playbin:
        message = 'Cannot instantiate gst "playbin" playbin.'
        logger.error(message)
        raise RuntimeError(message)

    pipeline.add(playbin)

    bus = pipeline.get_bus()

    loop.create_task(pool_messages())
    loop.create_task(fetch_position())


def destroy():
    pipeline.set_state(Gst.State.NULL)


async def pool_messages():
    interval = config.get('input_interval', 0.02)
    while True:
        await asyncio.sleep(interval)
        message = True
        while message:
            message = bus.pop()
            if message:
                on_message(message)


async def fetch_position():
    while True:
        await asyncio.sleep(0.5)
        if playing:
            success, position = playbin.query_position(Gst.Format.TIME)
            if success:
                playback.progress.on_next(position / Gst.SECOND)


def set_track(track):
    pipeline.set_state(Gst.State.READY)
    playbin.set_property('uri', track.uri)


def seek(position):
    playbin.seek_simple(
        Gst.Format.TIME,
        Gst.SeekFlags.FLUSH,
        position * Gst.SECOND,
    )


def play():
    global playing
    pipeline.set_state(Gst.State.PLAYING)
    playing = True
    playback.state.on_next('playing')


def pause():
    global playing
    pipeline.set_state(Gst.State.PAUSED)
    playback.state.on_next('paused')
    playing = False


def on_eos(*args):
    global playing
    playback.end_of_track.on_next(None)
    playing = False


def on_error():
    global playing
    logger.error('GST error :(')
    errors.on_next(None)
    playback.end_of_track.on_next(None)
    playing = False


def on_duration_changed():
    success, duration = playbin.query_duration(Gst.Format.TIME)
    if success:
        playback.duration.on_next(duration / Gst.SECOND)


def on_message(message):
    # structure = message.get_structure()
    # logger.debug('MESSAGE {}'.format(message.type))
    if message.type == Gst.MessageType.DURATION_CHANGED:
        on_duration_changed()

    elif message.type == Gst.MessageType.EOS:
        on_eos()

    elif message.type == Gst.MessageType.ERROR:
        on_error()

    # if structure:
        # structure_name = structure.get_name()
        # logger.debug('structure {}'.format(structure_name))
        # for i in range(structure.n_fields()):
        #     field_name = structure.nth_field_name(i)
        #     field_value = structure[field_name]
        #     logger.debug('{}: {}'.format(field_name, field_value))
        #     if field_value.__class__ == Gst.TagList:
        #         logger.debug(field_value.to_string())
                # logger.debug(field_value.__dict__)
                # for j in range(field_value.n_tags()):
                #     tag_name = field_value.nth_tag_name(j)
                #     tag_value = field_value.get_value(tag_name)
                #     logger.debug('{}: {}'.format(tag_name, tag_value))
