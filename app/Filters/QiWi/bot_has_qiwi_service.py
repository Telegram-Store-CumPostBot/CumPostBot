from aiogram.filters import BaseFilter
from aiogram.types import Message


class BotHasQiWiService(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        a = message.author_signature
        print(a)
        return True
