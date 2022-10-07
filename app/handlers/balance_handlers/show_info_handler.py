from string import Template
from typing import Any

from aiogram import Router
from aiogram.filters import Text

from data_models.user_models import MoneyUserInfo
from database.engine import async_session
from database.models.api.customer import DBAPICustomer
from keyboards.main_menu_keyboard import MainMenuKeyboard
from logger import get_logger

from handlers.template_handlers.message_handler_template import (
    MessageHandlerTemplate,
)
from settings.message_constants import BALANCE_INFO

router = Router()


balance_template = Template(
    '''
◉───────────────◉
 │  🆔*Ваш ID*: `$id`
 │  💰*Баланс:* `$balance`

 │  🤑*Реф\\. отчисления:* `$ref_payments`
 │  🧾*Сумма покупок:* `$total`
◉───────────────◉'''
)


@router.message(Text(text=[BALANCE_INFO]))
class ShowBalanceInfoHandler(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info('bot_id=%d username=%s chat_id=%d press "/BALANCE_INFO"',
                 self.bot.id, self.chat.username, self.chat.id)

        await self.clear_state()
        bal_info = await self.__get_balance_info()
        msg_text = self.__generate_profile_message(bal_info)

        return await self.event.answer(
            text=msg_text,
            reply_markup=MainMenuKeyboard().get(),
            parse_mode="MarkdownV2",
        )

    async def __get_balance_info(
            self,
    ) -> MoneyUserInfo:
        async with async_session() as session:
            return await DBAPICustomer.get_balance(
                session=session,
                chat_id=self.chat.id,
                bot_id=self.bot.id
            )

    def __generate_profile_message(self, bal_info: MoneyUserInfo) -> str:
        return balance_template.substitute(
                {
                    'id': self.chat.id,
                    'balance': bal_info.total_balance,
                    'ref_payments': bal_info.referral_fees,
                    'total': bal_info.sum_orders,
                }
            )
