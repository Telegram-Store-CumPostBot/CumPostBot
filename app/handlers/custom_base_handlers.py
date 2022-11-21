import asyncio

from abc import ABC, abstractmethod
from typing import cast, Any, Optional, Union, List, Coroutine

from aiogram.handlers import MessageHandler
from aiogram.types import (
    UNSET,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply
)

from update_aiogram.client.bot import Bot


class CustomMessageHandler(MessageHandler, ABC):
    def __init__(self, event, **kwargs: Any):
        self._middleware: List[Coroutine] = []
        super().__init__(event, **kwargs)

    async def _send_bot_deleted_message(
            self,
            chat_id: int,
            text: str,
            parse_mode: Optional[str] = UNSET,
            disable_web_page_preview: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            reply_markup: Optional[
                Union[
                    InlineKeyboardMarkup,
                    ReplyKeyboardMarkup,
                    ReplyKeyboardRemove,
                    ForceReply
                ]
            ] = None,
    ):
        msg = await self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
        )
        self.bot.add_deleted_message(self.chat.id, msg.message_id)

    async def send_deleted_message(
        self,
        text: str,
        parse_mode: Optional[str] = UNSET,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply
            ]
        ] = None,
    ):
        msg = await self.event.answer(
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_markup=reply_markup
        )
        self.bot.add_deleted_message(
            self.chat.id, msg.message_id)

    @property
    def bot(self) -> Bot:
        if "bot" in self.data:
            return cast(Bot, self.data["bot"])
        return Bot.get_current(no_error=False)

    @abstractmethod
    async def work(self) -> Any:
        pass

    async def handle(self) -> Any:
        await asyncio.gather(*self._middleware)
        await self.work()
