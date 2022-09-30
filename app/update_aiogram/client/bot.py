from typing import Optional

from aiogram import Bot as AiogramBot
from aiogram.client.session.base import BaseSession
from glQiwiApi import QiwiWrapper


class Bot(AiogramBot):
    def __init__(
            self,
            token: str,
            session: Optional[BaseSession] = None,
            parse_mode: Optional[str] = None,
            qiwi_wrapper: Optional[QiwiWrapper] = None,
    ) -> None:
        self.qiwi_wrapper = qiwi_wrapper

        self.deleted_messages = {}
        super().__init__(token, session, parse_mode)
