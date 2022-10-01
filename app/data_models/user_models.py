from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    chat_id: int
    tg_bot_id: int


class MoneyUserInfo(BaseUser):
    balance: float
    fake_balance: float = Field(alias='fake_bal')
    sum_orders: float
    referral_fees: float = Field(alias='ref_fees')

    @property
    def total_balance(self):
        return self.balance + self.fake_balance


class ProfileInfo(BaseUser):
    username: str
    first_name: str
    last_name: str
    referrals_count: int = Field(alias='ref_count')
