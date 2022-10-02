from typing import Optional

from aiogram import Bot as AiogramBot
from aiogram.client.session.base import BaseSession
from glQiwiApi import QiwiWrapper

from data_models.message import Message


class Bot(AiogramBot):
    def __init__(
            self,
            token: str,
            session: Optional[BaseSession] = None,
            parse_mode: Optional[str] = None,
            qiwi_wrapper: Optional[QiwiWrapper] = None,
    ) -> None:
        self.qiwi_wrapper = qiwi_wrapper

        self.__deleted_messages = {}
        super().__init__(token, session, parse_mode)

    def add_deleted_message(
            self,
            user_id: int,
            message_id: int,
    ):
        user_messages = self.__deleted_messages.get(user_id, [])
        msg = Message(chat_id=user_id, message_id=message_id)
        user_messages.append(msg)
        self.__deleted_messages[user_id] = user_messages

    def get_deleted_message(self, user_id: int) -> list[Message]:
        return self.__deleted_messages.get(user_id, [])

    def clear_deleted_message(self, user_id: int):
        self.__deleted_messages[user_id] = []
