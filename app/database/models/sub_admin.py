from typing import Optional

from ormar import Model, Integer, ForeignKey
from database.connection import BaseMeta
from database.models.tg_bot import TGBot


class SubAdmin(Model):
    class Meta(BaseMeta):
        tablename = "sub_admins"

    id: int = Integer(primary_key=True)
    chat_id: int = Integer(nullable=False)

    tg_bot: Optional[TGBot] = ForeignKey(TGBot)
