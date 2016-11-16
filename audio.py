import asyncio
import logging
import threading

logger = logging.getLogger('audio')

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject
from gi.repository import Gst

import playback

playbin = None
pipeline = None
bus = None
loop = None


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


async def pool_messages():
    while True:
        await asyncio.sleep(0.02)
        message = True
        while message:
            message = bus.pop()
            if message:
                on_message(message)


async def fetch_position():
    while True:
        await asyncio.sleep(0.5)
        success, position = playbin.query_position(Gst.Format.TIME)
        if success:
            playback.progress.on_next(position / Gst.SECOND)


def set_track(track):
    pipeline.set_state(Gst.State.READY)
    playbin.set_property('uri', track.uri)


def seek():
    playbin.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, 75 * Gst.SECOND)


def play():
    pipeline.set_state(Gst.State.PLAYING)
    loop.create_task(fetch_position())


def pause():
    logger.info('PAUSE')
    # pipeline.set_state(Gst.State)


def on_eos(*args):
    playback.end_of_track.on_next(None)


def on_error(*args):
    logger.error(args)


def on_progress(*args):
    logger.error(args)


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
