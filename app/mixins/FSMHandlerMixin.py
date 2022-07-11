from typing import Optional

from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.handler import BaseHandlerMixin
from aiogram.types import Message


class FSMHandlerMixin(BaseHandlerMixin[Message]):
    @property
    def state(self) -> Optional[FSMContext]:
        if "state" in self.data:
            return self.data['state']
        return None
