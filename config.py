import json
import logging

with open('config.json') as config_file:
    config = json.loads(config_file.read())

logging.basicConfig(
    filename=config['logFile'],
    level=logging._nameToLevel[config['logLevel']],
    format='%(levelname)s:%(name)s %(asctime)s %(message)s',
)


def get_keybindings():
    if not config:
        raise ValueError('Config is not initialized yet')
    return config.get('keybindings', [])
