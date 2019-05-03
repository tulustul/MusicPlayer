import logging
from typing import Any, Callable, Dict

logger = logging.getLogger('dependency injection')


class Injector:

    providers: Dict[Any, Callable] = {}

    def provide(self, token: Any, provider: Callable):
        self.providers[token] = provider

    def get(self, token: Any):
        if token not in self.providers:
            logger.error(f'Cannot find provider for {token}')

        value = self.providers[token]()

        if value is None:
            logger.error(f'Provider for {token} returned None')

        return value
