import asyncio
import logging

from commands.decorator import command
from ui.window import Window
from ui.components.progress import ProgressComponent

logger = logging.getLogger('plugins.test')


@command()
async def test_input(window: Window):
    text = await window.input('ola!')
    logger.info(f'test_input: {text}')


@command()
async def test_error(window: Window):
    window.show_error('dupa!')


@command()
async def test_progress(window: Window):
    progress_component = ProgressComponent()
    progress_component.set_text('progress', '')

    window.add_notification(progress_component)

    while progress_component.progress < 1:
        await asyncio.sleep(0.2)
        progress_component.progress += 0.05

    progress_component.detach()
