import logging

from commands.decorator import command
from ui.window import Window

logger = logging.getLogger('search')


@command()
async def search(window: Window):
    query = await window.input('Search:')
    window.active_component.filter(query)
