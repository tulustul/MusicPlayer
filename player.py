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
    from config import config
    import plugging
    import audio
    import ui
    import bindings
    import library
    import context
except Exception as e:
    log_exception()
else:
    if __name__ == '__main__':
        crashed = False
        loop = None
        try:
            setproctitle.setproctitle('music-player')

            loop = asyncio.get_event_loop()

            if config['logLevel'] == 'DEBUG':
                loop.set_debug(True)

            ui.init()
            audio.init(loop)
            plugging.init(loop)
            bindings.init()
            library.init()
            ui.initialize()

            context.push(config['default_context'])

            loop.run_until_complete(ui.win.process_input())
        except Exception as e:
            crashed = True
            log_exception()
        finally:
            plugging.destroy()
            ui.destroy()
            audio.destroy()
            for task in asyncio.Task.all_tasks():
                task.cancel()
            try:
                if loop:
                    loop.run_until_complete(
                        asyncio.gather(*asyncio.Task.all_tasks())
                    )
            except asyncio.CancelledError:
                pass
            finally:
                if loop:
                    loop.close()
                if crashed:
                    sys.exit(1)
