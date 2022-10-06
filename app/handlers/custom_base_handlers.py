from abc import ABC, abstractmethod
from typing import cast, Any

from aiogram.handlers import MessageHandler

from update_aiogram.client.bot import Bot


class CustomMessageHandler(MessageHandler, ABC):
    @property
    def bot(self) -> Bot:
        if "bot" in self.data:
            return cast(Bot, self.data["bot"])
        return Bot.get_current(no_error=False)

    @abstractmethod
    async def work(self) -> Any:
        pass

    async def handle(self) -> Any:
        await self.work()
