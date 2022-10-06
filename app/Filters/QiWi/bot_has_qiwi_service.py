from aiogram.filters import BaseFilter
from aiogram.types import Message


class BotHasQiWiService(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        a = message.get_current()
        print(a)
        return True
