from rx.subjects import ReplaySubject

import errors

context_stack = []

switch = ReplaySubject(1)

available_contexts = set()

current_context = None


def register(context):
    available_contexts.add(context)


def push(new_context):
    global current_context
    if new_context in available_contexts:
        current_context = new_context
        context_stack.append(new_context)
        switch.on_next(new_context)
    else:
        errors.push('Tried to push unknown context: "{}"'.format(new_context))


def pop():
    global current_context
    if context_stack:
        last_context = context_stack.pop()
        current_context = last_context
        switch.on_next(last_context)
