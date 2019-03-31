import asyncio

import ui

from .decorator import command


@command()
async def refresh():
    await asyncio.sleep(1)
    ui.win.refresh()
