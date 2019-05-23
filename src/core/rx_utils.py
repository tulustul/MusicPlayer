from asyncio import Future

from rx import operators as ops
from rx import Observable


# from https://github.com/ReactiveX/RxPY/blob/master/examples/asyncio/toasynciterator.py  # noqa
def to_async_iterable():
    def _to_async_iterable(source: Observable):
        class AIterable:
            def __aiter__(self):
                class AIterator:
                    def __init__(self):
                        self.notifications = []
                        self.future = Future()

                        source.pipe(ops.materialize()).subscribe(self.on_next)

                    def feeder(self):
                        if not self.notifications or self.future.done():
                            return

                        notification = self.notifications.pop(0)
                        dispatch = {
                            "N": lambda: self.future.set_result(
                                notification.value
                            ),
                            "E": lambda: self.future.set_exception(
                                notification.exception
                            ),
                            "C": lambda: self.future.set_exception(
                                StopAsyncIteration
                            ),
                        }

                        dispatch[notification.kind]()

                    def on_next(self, notification):
                        self.notifications.append(notification)
                        self.feeder()

                    async def __anext__(self):
                        self.feeder()

                        value = await self.future
                        self.future = Future()
                        return value

                return AIterator()

        return AIterable()

    return _to_async_iterable
