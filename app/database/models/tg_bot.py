from typing import Optional

from ormar import Model, Integer, String, Text, ForeignKey
from database.connection import BaseMeta
from database.models.admin import Admin


class TGBot(Model):
    class Meta(BaseMeta):
        tablename = "tg_bots"

    id: int = Integer(primary_key=True)
    tg_token: int = String(max_length=46, nullable=False)
    start_message: str = Text(nullable=True)

    admin: Optional[Admin] = ForeignKey(Admin)
