import logging
from collections import namedtuple
from typing import Dict, List, Optional, cast

from rx.subjects import Subject, ReplaySubject

from core import errors

logger = logging.getLogger('context')

Context = namedtuple('Context', ['name', 'on_enter', 'on_exit'])

context_stack: List[Context] = []

switch = ReplaySubject(1)

contexts: Dict[str, Context] = {}

current_context: Optional[Context] = None


def register(context_name: str):
    new_context = Context(
        name=context_name,
        on_enter=Subject(),
        on_exit=Subject(),
    )

    contexts[context_name] = new_context
    return new_context


def get_context(context_name: str):
    if context_name not in contexts:
        return register(context_name)
    return contexts.get(context_name)


def push(context_name: str):
    global current_context

    new_context = get_context(context_name)

    if not new_context:
        errors.push('Tried to push unknown context: "{}"'.format(context_name))
        return

    if current_context:
        current_context.on_exit.on_next(current_context)

    current_context = new_context
    _current_context = cast(Context, current_context)

    context_stack.append(_current_context)
    _current_context.on_enter.on_next(current_context)
    switch.on_next(current_context)


def pop():
    global current_context
    if len(context_stack) >= 2:
        current_context.on_exit.on_next(current_context)

        context_stack.pop()
        current_context = context_stack[-1]
        current_context.on_enter.on_next(current_context)
        switch.on_next(current_context)
