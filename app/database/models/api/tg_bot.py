from typing import Optional

from database.models.api.tg_bot_methods.check_availability import \
    check_availability
from database.models.api.tg_bot_methods.create_new import create_new
from database.models.api.tg_bot_methods.get_qiwi_txn import get_qiwi_txn
from database.models.api.tg_bot_methods.set_qiwi_txn import set_qiwi_txn
from database.models.tables.tg_bot import TGBot


class DBAPITGBot:
    @classmethod
    async def get_qiwi_txn(cls, tg_bot_id: int) -> Optional[int]:
        return await get_qiwi_txn(tg_bot_id)

    @classmethod
    async def set_qiwi_txn(cls, tg_bot_id: int, qiwi_txn: int) -> bool:
        return await set_qiwi_txn(tg_bot_id, qiwi_txn)

    @classmethod
    async def check_availability(cls, tg_bot_id: int) -> bool:
        return await check_availability(tg_bot_id)

    @classmethod
    async def create_new(
            cls,
            tg_bot_id: int,
            tg_bot_token: str,
            start_message: Optional[str] = None,
            qiwi_txn: Optional[int] = None,
            admin_id: Optional[int] = None,
    ) -> TGBot:
        return await create_new(
            tg_bot_id,
            tg_bot_token,
            start_message,
            qiwi_txn,
            admin_id
        )
