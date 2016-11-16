from rx.subjects import Subject

KEY_CODES = {
    '<home>': 262,
    '<end>': 360,
    '<pagedown>': 338,
    '<pageup>': 339,
    '<backspace>': 263,
    '<space>': 32,
    '<enter>': '\n',
    '<tab>': 9,
    '<esc>': 27,
    '<delete>': 330,
    '<insert>': 331,
    '<arrowdown>': 258,
    '<arrowup>': 259,
    '<arrowleft>': 260,
    '<arrowright>': 261,
    '<f1>': 265,
    '<f2>': 266,
    '<f3>': 267,
    '<f4>': 268,
    '<f5>': 269,
    '<f6>': 270,
    '<f7>': 271,
    '<f8>': 272,
    '<f9>': 273,
    '<f10>': 274,
    '<f11>': 275,
    '<f12>': 276,
}

KEY_CODES_REVERSED = {code: name for name, code in KEY_CODES.items()}


def tranform_code(key):
    try:
        default = chr(key) if isinstance(key, int) else key
        return KEY_CODES_REVERSED.get(key, default)
    except:
        return ''


raw_keys = Subject()
keys = raw_keys.map(tranform_code)
