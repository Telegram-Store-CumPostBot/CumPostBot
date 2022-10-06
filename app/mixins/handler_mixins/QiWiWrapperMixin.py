from typing import Optional, cast

from aiogram.handlers import BaseHandlerMixin
from aiogram.types import Message
from glQiwiApi import QiwiWrapper

from update_aiogram.client.bot import Bot


class QiWiWrapperMixin(BaseHandlerMixin[Message]):
    @property
    def qiwi_wrapper(self) -> Optional[QiwiWrapper]:
        if "bot" in self.data and isinstance(cast(Bot, self.data["bot"]), Bot):
            return cast(Bot, self.data["bot"]).qiwi_wrapper
        return None
