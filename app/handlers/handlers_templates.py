from typing import Any

from aiogram.dispatcher.handler import MessageHandler
from abc import ABC, abstractmethod
from aiogram import flags

from mixins.FSMHandlerMixin import FSMHandlerMixin


class MessageHandlerTemplate(MessageHandler, FSMHandlerMixin, ABC):
    @property
    @abstractmethod
    def handle_flags(self):
        return {
            'throttling_key': None,
            'throttle_time': None
        }

    @abstractmethod
    async def work(self) -> Any:
        pass

    @flags.rate_limit(handle_flags)
    async def handle(self) -> Any:
        await self.work()
