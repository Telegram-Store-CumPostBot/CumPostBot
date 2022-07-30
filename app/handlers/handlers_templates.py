from typing import Any

from aiogram.dispatcher.handler import MessageHandler
from abc import ABC, abstractmethod
from aiogram import flags

from middlewares.middlewares_settings import ThrottlingSettings
from mixins.FSMHandlerMixin import FSMHandlerMixin


@flags.rate_limit(ThrottlingSettings.DEFAULT_FLAGS)
class MessageHandlerTemplate(MessageHandler, FSMHandlerMixin, ABC):
    @abstractmethod
    async def work(self) -> Any:
        pass

    async def handle(self) -> Any:
        await self.work()
