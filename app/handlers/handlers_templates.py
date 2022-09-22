from typing import Any, cast

from aiogram.dispatcher.handler import MessageHandler
from abc import ABC, abstractmethod
from aiogram import flags

from middlewares.middlewares_settings import ThrottlingSettings
from mixins.FSMHandlerMixin import FSMHandlerMixin
from update_aiogram.client.bot import Bot


@flags.rate_limit(ThrottlingSettings.DEFAULT_FLAGS)
class MessageHandlerTemplate(MessageHandler, FSMHandlerMixin, ABC):
    @abstractmethod
    async def work(self) -> Any:
        pass

    async def handle(self) -> Any:
        await self.work()

    @property
    def bot(self) -> Bot:
        if "bot" in self.data:
            return cast(Bot, self.data["bot"])
        return Bot.get_current(no_error=False)
