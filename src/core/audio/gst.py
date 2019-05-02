import asyncio
import logging
import threading

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject
from gi.repository import Gst

from core.config import config
from core.errors import errors
from plugins.library.models import Track

from .audio_backend import AudioBackend

logger = logging.getLogger('audio')


class GstAudioBackend(AudioBackend):

    def __init__(self):
        super().__init__()

        GObject.threads_init()
        Gst.init(None)

        self.pipeline = Gst.Pipeline()

        self.playbin = Gst.ElementFactory.make('playbin', None)
        if not self.playbin:
            message = 'Cannot instantiate gst "playbin" playbin.'
            logger.error(message)
            raise RuntimeError(message)

        self.pipeline.add(self.playbin)

        self.bus = self.pipeline.get_bus()

        loop = asyncio.get_event_loop()

        loop.create_task(self.pool_messages())
        loop.create_task(self.fetch_position())

    def destroy(self):
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)

    def set_track(self, track: Track):
        self.pipeline.set_state(Gst.State.READY)
        self.playbin.set_property('uri', track.uri)
        self.duration.on_next(track.length)
        self.position.on_next(0)

    def seek(self, position: int):
        self.playbin.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH,
            position * Gst.SECOND,
        )
        self.position.on_next(position)

    def play(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.playing = True
        self.state.on_next(self.State.playing)

    def pause(self):
        self.pipeline.set_state(Gst.State.PAUSED)
        self.playing = False
        self.state.on_next(self.State.paused)

    async def pool_messages(self):
        interval = config.get('input_interval', 0.02)
        while True:
            await asyncio.sleep(interval)
            message = True
            while message:
                message = self.bus.pop()
                if message:
                    self.on_message(message)

    async def fetch_position(self):
        while True:
            await asyncio.sleep(0.5)
            if self.playing:
                success, position = self.playbin.query_position(Gst.Format.TIME)
                if success:
                    self.position.on_next(position / Gst.SECOND)

    def on_eos(self, *args):
        self.playing = False
        self.end_of_track.on_next(None)

    def on_error(self):
        logger.error('GST error :(')
        self.pipeline.set_state(Gst.State.NULL)
        self.playing = False
        errors.on_next(None)
        self.end_of_track.on_next(None)

    def on_duration_changed(self):
        success, duration = self.playbin.query_duration(Gst.Format.TIME)
        if success:
            self.duration.on_next(duration / Gst.SECOND)

    def on_message(self, message):
        # structure = message.get_structure()
        # logger.debug('MESSAGE {}'.format(message.type))
        if message.type == Gst.MessageType.DURATION_CHANGED:
            self.on_duration_changed()

        elif message.type == Gst.MessageType.EOS:
            self.on_eos()

        elif message.type == Gst.MessageType.ERROR:
            self.on_error()

        # if structure:
            # structure_name = structure.get_name()
            # logger.debug('structure {}'.format(structure_name))
            # for i in range(structure.n_fields()):
            #    `` field_name = structure.nth_field_name(i)
            #     field_value = structure[field_name]
            #     logger.debug('{}: {}'.format(field_name, field_value))
            #     if field_value.__class__ == Gst.TagList:
            #         logger.debug(field_value.to_string())
                    # logger.debug(field_value.__dict__)
                    # for j in range(field_value.n_tags()):
                    #     tag_name = field_value.nth_tag_name(j)
                    #     tag_value = field_value.get_value(tag_name)
                    #     logger.debug('{}: {}'.format(tag_name, tag_value))
