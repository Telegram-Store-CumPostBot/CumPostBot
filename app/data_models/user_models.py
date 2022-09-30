from pydantic import BaseModel


class BaseUser(BaseModel):
    chat_id: int
    tg_bot_id: int


class MoneyUserInfo(BaseUser):
    balance: float
    fake_balance: float
    sum_orders: float
    referral_fees: float

    @property
    def total_balance(self):
        return self.balance + self.fake_balance


class ProfileInfo(BaseUser):
    username: str
    first_name: str
    last_name: str
    referrals_count: int
