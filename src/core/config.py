import logging
import os
from pathlib import Path
from typing import Sequence, Union

import commentjson
from mypy_extensions import TypedDict

Keybinding = TypedDict('Keybinding', {
    'keys': Sequence[str],
    'command': str,
    'context': str,
    'args': Sequence[Union[float, int, str, list, dict]],
})

home = Path.home()
Path(f'{home}/.config/music-player').mkdir(parents=True, exist_ok=True)

path = os.path.dirname(__file__) + '/..'

with open(f'{path}/config.json') as config_file:
    config: dict = commentjson.loads(config_file.read())

theme = config['theme']

with open(f'{path}/themes/{theme}.json') as theme_file:
    theme = commentjson.loads(theme_file.read())

logging.basicConfig(
    filename=Path(config['log_file']).expanduser(),
    level=logging._nameToLevel[config['log_level']],
    format='%(levelname)s:%(name)s %(asctime)s %(message)s',
)

rx_logger = logging.getLogger('Rx')
rx_logger.setLevel(logging.INFO)


def get_keybindings() -> Sequence[Keybinding]:
    if not config:
        raise ValueError('Config is not initialized yet')
    return config.get('keybindings', [])
