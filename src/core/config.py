import logging
import os
from pathlib import Path
from typing import Sequence, Union

import commentjson
from mypy_extensions import TypedDict


def deep_merge_dicts(dict_a: dict, dict_b: dict, target=None):
    # dict_b have priority in case of confict

    if target is None:
        target = {}

    keys = set(dict_a.keys()) | set(dict_b.keys())
    for key in keys:
        if key in dict_a and key in dict_b:
            value_a = dict_a[key]
            value_b = dict_b[key]
            type_a, type_b = type(value_a), type(value_b)
            if type_a != type_b:
                message = f'config error: "{key}" should have type "{type_a}"'
                raise ValueError(message)

            if isinstance(value_a, dict):
                target[key] = {}
                deep_merge_dicts(value_a, value_b, target[key])
            elif isinstance(value_a, list):
                target[key] = value_a + value_b
            else:
                target[key] = value_b
        elif key in dict_a:
            target[key] = dict_a[key]
        else:
            target[key] = dict_b[key]
    return target


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
    default_config: dict = commentjson.loads(config_file.read())

with open(f'{home}/.config/music-player/config.json') as config_file:
    user_config: dict = commentjson.loads(config_file.read())

config = deep_merge_dicts(default_config, user_config)

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
