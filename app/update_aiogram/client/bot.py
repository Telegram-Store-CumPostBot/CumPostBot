from typing import Optional

from aiogram import Bot as AiogramBot
from aiogram.client.session.base import BaseSession

from data_models.message import Message
from services.payment_services.QiWi.qiwi_payment_service import \
    QiWiPaymentService


class Bot(AiogramBot):
    def __init__(
            self,
            token: str,
            session: Optional[BaseSession] = None,
            parse_mode: Optional[str] = None,
            qiwi_access_token: str = None,
            qiwi_phone_with_plus: str = None,
    ) -> None:
        self.__deleted_messages = {}
        super().__init__(token, session, parse_mode)

        self._qiwi_service = None
        if qiwi_access_token and qiwi_phone_with_plus:
            self._qiwi_service = QiWiPaymentService(
                access_token=qiwi_access_token,
                phone=qiwi_phone_with_plus,
                tg_bot_id=self.id
            )

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
