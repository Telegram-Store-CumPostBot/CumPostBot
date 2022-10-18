import asyncio
from typing import Any

from aiogram import Router, flags
from aiogram.filters import Text

from data_models.user_notify import UserNotifications
from decorators.handler_decorators.will_delete_user_message import (
    will_delete_user_message,
)

from logger import get_logger

from handlers.template_handlers.message_handler_template import (
    MessageHandlerTemplate,
)
from services.payment_services.QiWi.qiwi_payment_service import (
    QiWiPaymentService,
)
from settings.message_constants import CHECK_BALANCE
from settings.settings import config, settings


router = Router()


@router.message(Text(text=[CHECK_BALANCE]))
@flags.rate_limit({config['FlagsNames']['throttling_key']: 'check_balance',
                   config['FlagsNames']['throttle_time']: 3})
@will_delete_user_message
class CheckNewPaymentsHandler(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info('bot_id=%d username=%s chat_id=%d press "/CHECK_PAYMENTS"',
                 self.bot.id, self.chat.username, self.chat.id)
        await self.clear_state()

        notifications: UserNotifications = await QiWiPaymentService(
            settings.qiwi_access_token,
            settings.qiwi_phone,
            self.bot.id
        ).check_new_payments()

        tasks = [self.bot.send_message(n.chat_id, n.message, parse_mode='HTML')
                 for n in notifications]
        await asyncio.gather(*tasks)
        if not tasks:
            await self.send_deleted_message(
                'Не обнаружили пополнений((', parse_mode='HTML')
