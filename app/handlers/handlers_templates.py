from typing import Any

from abc import ABC, abstractmethod
from aiogram import flags

from handlers.custom_base_handlers import CustomMessageHandler
from middlewares.middlewares_settings import ThrottlingSettings
from mixins.FSMHandlerMixin import FSMHandlerMixin
from mixins.UpdateBotMixin import UpdateBotMixin


@flags.rate_limit(ThrottlingSettings.DEFAULT_FLAGS)
class MessageHandlerTemplate(CustomMessageHandler, FSMHandlerMixin, UpdateBotMixin, ABC):
    @abstractmethod
    async def work(self) -> Any:
        pass

    async def handle(self) -> Any:
        await self.work()
