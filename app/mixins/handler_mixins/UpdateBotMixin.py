from typing import cast

from aiogram.handlers import BaseHandlerMixin
from aiogram.types import Message

from update_aiogram.client.bot import Bot


class UpdateBotMixin(BaseHandlerMixin[Message]):
    @property
    def bot(self) -> Bot:
        if "bot" in self.data:
            return cast(Bot, self.data["bot"])
        return Bot.get_current(no_error=False)
