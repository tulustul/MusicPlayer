from rx.subjects import Subject

import errors

context_stack = []

context = Subject()

available_contexts = []


def register(context):
    available_contexts.append(context)


def push(new_context):
    if new_context in available_contexts:
        context_stack.append(new_context)
        context.on_next(new_context)
    else:
        errors.push('Tried to push unknown context: "{}"'.format(new_context))


def pop():
    if context_stack:
        last_context = context_stack.pop()
        context.on_next(last_context)
