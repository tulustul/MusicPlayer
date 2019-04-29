import asyncio
import logging

from commands.decorator import command
from ui.window import Window
from ui.components.progress import ProgressComponent
from player_ui import PlayerUI

logger = logging.getLogger('plugins.test')


@command()
async def test_input(window: Window):
    text = await window.input('ola!')
    logger.info(f'test_input: {text}')


@command()
async def test_error(ui: PlayerUI):
    ui.show_error('dupa!')


@command()
async def test_progress(ui: PlayerUI, window: Window):
    progress_component = ProgressComponent()
    progress_component.set_text('progress', '')

    ui.stack_layout.add(progress_component)
    window.root_component.update_layout()

    while progress_component.progress < 1:
        await asyncio.sleep(0.2)
        progress_component.progress += 0.05

    progress_component.detach()
