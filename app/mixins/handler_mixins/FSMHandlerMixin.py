from abc import ABC, abstractmethod
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.handlers import BaseHandlerMixin
from aiogram.types import Message

from logger import get_logger


class FSMHandlerMixin(BaseHandlerMixin[Message], ABC):
    @property
    @abstractmethod
    def bot(self):
        pass

    @property
    @abstractmethod
    def chat(self):
        pass

    @property
    def state(self) -> Optional[FSMContext]:
        if "state" in self.data:
            return self.data['state']
        return None

    async def clear_state(self):
        log = get_logger(__name__)
        current_state = await self.state.get_state()
        if self.state and current_state is not None:
            log.debug(
                'in bot_id=%d user with username=%s and '
                'chat_id=%d: canceling state: %s',
                self.bot.id, self.chat.username, self.chat.id, current_state)
            await self.state.clear()
