from dataclasses import dataclass
from typing import Dict
from types import FunctionType


@dataclass
class Command:
    func: FunctionType
    name: str
    display_name: str
    visible_in_palette: bool


by_name: Dict[str, Command] = {}
by_display_name: Dict[str, Command] = {}


def register(
    func: FunctionType, name: str, display_name: str, visible_in_palette: bool
):
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
