from typing import Optional

from database.models.api.tg_bot_methods.get_qiwi_txn import get_qiwi_txn
from database.models.api.tg_bot_methods.set_qiwi_txn import set_qiwi_txn


class DBAPITGBot:
    @classmethod
    async def get_qiwi_txn(cls, tg_bot_id: int) -> Optional[int]:
        return await get_qiwi_txn(tg_bot_id)

    @classmethod
    async def set_qiwi_txn(cls, tg_bot_id: int, qiwi_txn: int) -> bool:
        return await set_qiwi_txn(tg_bot_id, qiwi_txn)
