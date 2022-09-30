from typing import Optional

from pydantic import BaseModel


class TGUser(BaseModel):
    chat_id: Optional[int]
    balance: Optional[float]
    fake_balance: Optional[float]
    sum_orders: Optional[float]
    referrals_count: Optional[float]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
