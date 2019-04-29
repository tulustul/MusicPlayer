import curses
from rx.subjects import Subject
from rx.operators import map


def get_curses_key_definitions():
    return (
        (key, value) for key, value in vars(curses).items()
        if key.startswith('KEY_')
    )


def get_key_binding_name(key_name: str):
    # KEY_ENTER -> <enter>
    name = key_name[len('KEY_'):].lower()
    return f'<{name}>'


KEY_CODES = {
    key_value: get_key_binding_name(key_name)
    for key_name, key_value in get_curses_key_definitions()
}

# add some entries missing in curses definitions
KEY_CODES[10] = '<enter>'
KEY_CODES[27] = '<esc>'
KEY_CODES[32] = '<space>'

def tranform_code(key: int) -> str:
    try:
        default = chr(key)
        return KEY_CODES.get(key, default)
    except:
        return ''


raw_keys = Subject()
keys = raw_keys.pipe(map(tranform_code))
