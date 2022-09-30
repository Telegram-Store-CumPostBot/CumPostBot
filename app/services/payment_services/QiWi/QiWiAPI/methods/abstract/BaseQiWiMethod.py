from abc import ABC, abstractmethod
from typing import Coroutine


class BaseQiWiMethod(ABC):
    def build_method(self) -> Coroutine:
        return self._work()

    @abstractmethod
    async def _work(self):
        pass
