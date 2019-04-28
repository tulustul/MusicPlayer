from collections import OrderedDict
import logging
import pprint

from commands.decorator import command
from ui.window import Window
from ui.components.layout import Layout
from ui.components.component import AbstractComponent

logger = logging.getLogger('plugins.debug')


@command()
async def debug_dump_layout(window: Window):
    data = dump_layout_data(window.root_component)
    logger.debug('\n' + pprint.pformat(data))


def dump_layout_data(component: AbstractComponent):
    data: dict = OrderedDict(
        clazz=component.__class__.__name__,
        rect=component.rect,
        desired_size=component.desired_size,
    )
    if isinstance(component, Layout):
        data['childs'] = []
        for child in component.childs:
            data['childs'].append(dump_layout_data(child))

    return data
