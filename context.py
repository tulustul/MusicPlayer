import logging
from collections import namedtuple

from rx.subjects import Subject, ReplaySubject

import errors

logger = logging.getLogger('context')

Context = namedtuple('Context', ['name', 'on_enter', 'on_exit'])

context_stack = []

switch = ReplaySubject(1)

contexts = {}

current_context = None


def register(context_name):
    new_context = Context(
        name=context_name,
        on_enter=Subject(),
        on_exit=Subject(),
    )

    contexts[context_name] = new_context
    return new_context


def get_context(context_name):
    return contexts.get(context_name)


def push(context_name):
    global current_context

    new_context = get_context(context_name)

    if not new_context:
        errors.push('Tried to push unknown context: "{}"'.format(context_name))
        return

    if current_context:
        current_context.on_exit.on_next(current_context)

    current_context = new_context
    context_stack.append(current_context)
    current_context.on_enter.on_next(current_context)
    switch.on_next(current_context)


def pop():
    global current_context
    if len(context_stack) >= 2:
        current_context.on_exit.on_next(current_context)

        context_stack.pop()
        current_context = context_stack[-1]
        current_context.on_enter.on_next(current_context)
        switch.on_next(current_context)
