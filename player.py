import asyncio
import sys
import traceback
import logging

import setproctitle

import audio
import config  # initializing config by importing it
from errors import errors
import ui
from ui.window import Window
import bindings
import library

logger = logging.getLogger('player')

errors.subscribe(lambda e: logger.error(e))


# async def test_asyncio():
#     while True:
#         logger.warn('test_asyncio')
#         await asyncio.sleep(1)


if __name__ == '__main__':
    setproctitle.setproctitle('music-player')

    loop = asyncio.get_event_loop()

    window = Window()
    ui.set_window(window)
    audio.init(loop)
    bindings.init()
    library.init()

    try:
        # loop.create_task(test_asyncio())
        loop.run_until_complete(window.process_input())
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error(''.join(traceback.format_exception(
            exc_type, exc_value, exc_traceback,
        )))
    finally:
        window.destroy()
