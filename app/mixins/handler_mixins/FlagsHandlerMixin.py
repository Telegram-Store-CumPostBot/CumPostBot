from typing import Optional, Dict, Any

from aiogram.handlers import BaseHandlerMixin
from aiogram.types import Message


class FlagsHandlerMixin(BaseHandlerMixin[Message]):
    @property
    def flags(self) -> Optional[Dict[str, Any]]:
        handler = self.data['handler']

        if not hasattr(handler, "flags"):
            return {}
        return handler.flags
