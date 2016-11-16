from collections import namedtuple

Command = namedtuple('Command', [
    'func',
    'name',
    'display_name',
    'visible_in_palette',
])

by_name = {}
by_display_name = {}


def register(func, name, display_name, visible_in_palette):
    command = Command(
        func=func,
        name=name,
        display_name=display_name,
        visible_in_palette=visible_in_palette,
    )
    by_name[name] = command
    by_display_name[display_name] = command


def get_by_name(name):
    return by_name.get(name)


def get_by_display_name(display_name):
    return by_display_name.get(display_name)


def get_names():
    return sorted(by_name.keys())
