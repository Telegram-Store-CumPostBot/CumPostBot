import string
from typing import Any

from aiogram import Router, flags
from aiogram.filters import Text

from database.models.helpers.transform_tg_id import transform_tg_id
from decorators.handler_decorators.will_delete_user_message import (
    will_delete_user_message,
)

from logger import get_logger

from handlers.template_handlers.message_handler_template import (
    MessageHandlerTemplate,
)
from settings.message_constants import QIWI_DEPOSIT
from settings.settings import config, settings


router = Router()


message_template = string.Template('''
Для пополнения баланса переведите средства
☎на номер `${phone}`
💌с комментарием `${comment}`
''')


@router.message(Text(text=[QIWI_DEPOSIT]))
@flags.rate_limit({config['FlagsNames']['throttling_key']: 'deposit_balance',
                   config['FlagsNames']['throttle_time']: 2})
@will_delete_user_message
class DepositBalance(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info('bot_id=%d username=%s chat_id=%d press "/QIWI_DEPOSIT"',
                 self.bot.id, self.chat.username, self.chat.id)
        await self.clear_state()

        deposit_comment = str(transform_tg_id(self.bot.id))
        deposit_comment += str(transform_tg_id(self.chat.id))
        await self.send_deleted_message(text=self._generate_deposit_message())

    def _generate_deposit_message(self) -> str:
        deposit_comment = str(transform_tg_id(self.chat.id))
        deposit_comment += str(transform_tg_id(self.bot.id))

        return message_template.substitute({
            'phone': settings.qiwi_phone,
            'comment': deposit_comment,
        })
