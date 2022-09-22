from typing import Any, cast

from aiogram.dispatcher.handler import MessageHandler
from abc import ABC, abstractmethod
from aiogram import flags

from middlewares.middlewares_settings import ThrottlingSettings
from mixins.FSMHandlerMixin import FSMHandlerMixin
from mixins.UpdateBotMixin import UpdateBotMixin


@flags.rate_limit(ThrottlingSettings.DEFAULT_FLAGS)
class MessageHandlerTemplate(MessageHandler, FSMHandlerMixin, UpdateBotMixin, ABC):
    @abstractmethod
    async def work(self) -> Any:
        pass

    async def handle(self) -> Any:
        await self.work()
