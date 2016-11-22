from rx.subjects import Subject

errors = Subject()


def push(message):
    errors.on_next(message)
