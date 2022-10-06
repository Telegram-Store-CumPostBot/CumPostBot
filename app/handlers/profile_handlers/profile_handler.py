from string import Template
from typing import Any

from aiogram import Router, flags
from aiogram.filters import Text

from data_models.user_models import ProfileInfo, MoneyUserInfo
from database.engine import AsyncSessionTyping, async_session
from database.models.api.customer import DBAPICustomer
from decorators.handler_decorators.clear_inline_message import \
    clear_inline_message
from handlers.template_handlers.message_handler_template import \
    MessageHandlerTemplate
from logger import get_logger
from settings.message_constants import PROFILE
from settings.settings import config

router = Router()

profile_template = Template(
    '''
◉───────────────◉
 │  🆔*Ваш ID*: `$id`
 │  💰*Баланс:* `$balance`

 │  🤑*Реф\\. отчисления:* `$ref_payments`
 │  🧾*Сумма покупок:* `$total`
 │  👥*Рефералы:* `$referrals`
◉───────────────◉'''
)


@router.message(Text(text=[PROFILE]))
@flags.rate_limit({config['FlagsNames']['throttling_key']: 'profile',
                   config['FlagsNames']['throttle_time']: 1})
@clear_inline_message
class ProfileHandler(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info(
            'in bot_id=%d user with username=%s and'
            ' chat_id=%d logged in to the profile',
            self.bot.id, self.chat.username, self.chat.id
        )

        await self.clear_state()

        msg = await self.__generate_profile_message()
        user_id = self.from_user.id

        self.bot.add_deleted_message(user_id, msg.message_id)
        self.bot.add_deleted_message(user_id, self.event.message_id)
        return msg

    async def __generate_profile_message(
            self,
    ):
        async with async_session() as session:
            profile_info = await self.__get_profile_info(session)
            balance_info = await self.__get_balance_info(session)

        return await self.event.answer(
            text=profile_template.substitute(
                {
                    'balance': balance_info.total_balance,
                    'id': self.chat.id,
                    'referrals': profile_info.referrals_count,
                    'total': balance_info.sum_orders,
                    'ref_payments': balance_info.referral_fees
                }
            ),
            parse_mode="MarkdownV2"
        )

    async def __get_profile_info(
            self,
            session: AsyncSessionTyping
    ) -> ProfileInfo:
        return await DBAPICustomer.get_static_info(
            session=session,
            chat_id=self.chat.id,
            bot_id=self.bot.id
        )

    async def __get_balance_info(
            self,
            session: AsyncSessionTyping
    ) -> MoneyUserInfo:
        return await DBAPICustomer.get_balance(
            session=session,
            chat_id=self.chat.id,
            bot_id=self.bot.id
        )
