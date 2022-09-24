from string import Template
from typing import Any

from aiogram import Router, flags
from aiogram.dispatcher.filters import Text

from database.models.customer import Customer
from handlers.handlers_templates import MessageHandlerTemplate
from logger import get_logger
from settings.message_constants import PROFILE
from settings.settings import config

router = Router()

profile_template = Template(
    '''
◉───────────────◉
 │  🆔*Ваш ID*: `$id`            
 │  💰*Баланс:* `$balance`                       
 │                             
 │  🤑*Реф\. отчисления:* `$ref_payments`
 │  🧾*Сумма покупок:* `$total`  
 │  👥*Рефералы:* `$referrals`   
◉───────────────◉
    '''
)


@router.message(Text(text=[PROFILE]))
@flags.rate_limit({config['FlagsNames']['throttling_key']: 'profile', config['FlagsNames']['throttle_time']: 1})
class ProfileHandler(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info('in bot_id=%d user with username=%s and chat_id=%d logged in to the profile', self.bot.id, self.chat.username, self.chat.id)

        if self.state and (current_state := await self.state.get_state()) is not None:
            log.debug('in bot_id=%d user with username=%s and chat_id=%d: canceling state: %s', self.bot.id, self.chat.username, self.chat.id,
                      current_state)
            await self.state.clear()

        user: dict = await Customer.get_static_info(self.chat.id, self.bot.id)
        user.update(await Customer.get_balance(self.chat.id, self.bot.id))

        return await self.event.answer(
            text=profile_template.substitute(
                {
                    'balance': user['balance'] + user['fake_balance'],
                    'id': self.chat.id,
                    'referrals': user['referrals_count'],
                    'total': user['sum_orders'],
                    'ref_payments': user['referral_fees']
                }
            ),
            parse_mode="MarkdownV2"
        )
