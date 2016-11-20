import asyncio
import sys
import traceback
import logging

import setproctitle

from errors import errors

logger = logging.getLogger('player')

errors.subscribe(lambda e: logger.error(e))


def log_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logger.error(''.join(traceback.format_exception(
        exc_type, exc_value, exc_traceback,
    )))


try:
    import audio
    from config import config
    import ui
    from ui.window import Window
    import bindings
    import library
except Exception as e:
    log_exception()
else:
    if __name__ == '__main__':
        try:
            setproctitle.setproctitle('music-player')

            loop = asyncio.get_event_loop()

            if config['logLevel'] == 'DEBUG':
                loop.set_debug(True)

            window = Window()
            ui.set_window(window)
            audio.init(loop)
            bindings.init()
            library.init()

            loop.run_until_complete(window.process_input())
        except Exception as e:
            log_exception()
        finally:
            window.destroy()
            audio.destroy()
            for task in asyncio.Task.all_tasks():
                task.cancel()
            try:
                loop.run_until_complete(
                    asyncio.gather(*asyncio.Task.all_tasks())
                )
            except asyncio.CancelledError:
                pass
            finally:
                loop.close()
