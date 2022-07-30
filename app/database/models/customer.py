from typing import Optional, ForwardRef

from cashews import cache
from ormar import Model, Integer, ForeignKey, Float, String, IndexColumns

from logger import get_logger
from database.connection import BaseMeta
from database.models.tg_bot import TGBot
from settings.settings import config

CustomerRef = ForwardRef("Customer")


class Customer(Model):
    class Meta(BaseMeta):
        tablename = "customers"
        constraints = [IndexColumns('chat_id', postgresql_using='btree')]

    id: int = Integer(primary_key=True)
    balance: float = Float(nullable=False, default=0)
    fake_balance: float = Float(nullable=False, default=0)
    chat_id = Integer(nullable=False)
    sum_orders: float = Float(nullable=False, default=0)
    referrals_count: int = Integer(nullable=False, default=0)
    referral_fees: float = Float(nullable=False, default=0)
    username: str = String(max_length=32)
    first_name: str = String(max_length=64)
    last_name: str = String(max_length=64)

    refer: Optional[CustomerRef] = ForeignKey(CustomerRef, related_name="referes")
    tg_bot: Optional[TGBot] = ForeignKey(TGBot, related_name="tg_bots")

    @classmethod
    async def create_new(cls, **kwargs):
        return await create_user(**kwargs)

    @classmethod
    @cache(ttl=1_800_000, key='customer:availability:{chat_id}')
    async def check_availability(cls, chat_id: int) -> bool:
        print('попал')
        # использую без limit, чтобы сразу отловить наличие более одной копии и пофиксить такой трабл
        # user = await Customer.objects.filter(chat_id=self.chat.id).limit(1).values('id')
        user = await Customer.objects.filter(chat_id=chat_id).values('id')
        assert len(user) in (0, 1)
        if user:
            return True
        return False

    @classmethod
    @cache(ttl=float(config['CacheTimings']['user_balance']), key='customer:balance:{chat_id}')
    async def get_balance(cls, chat_id):
        user = await Customer.objects.filter(chat_id=chat_id).values(['balance', 'fake_balance', 'sum_orders', 'referral_fees'])
        user = user[0]
        return user

    @classmethod
    @cache(ttl=float(config['CacheTimings']['user_static_info']), key='customer:static_info:{chat_id}')
    async def get_static_info(cls, chat_id):
        log = get_logger(__name__)
        log.info('get static info about user chat_id: %d', chat_id)
        user = await Customer.objects.filter(chat_id=chat_id).values(['username', 'first_name', 'last_name', 'referrals_count'])
        user = user[0]
        user['chat_id'] = chat_id
        return user


@cache.invalidate(Customer.check_availability, {'chat_id': lambda kwargs: kwargs['chat_id']})
async def create_user(**kwargs):
    return await Customer(**kwargs).save()


Customer.update_forward_refs()
