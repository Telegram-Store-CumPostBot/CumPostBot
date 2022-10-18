from typing import Any

from aiogram import Router, flags
from aiogram.filters import Text

from decorators.handler_decorators.clear_inline_message import (
    clear_inline_message,
)
from decorators.handler_decorators.will_delete_user_message import (
    will_delete_user_message,
)
from keyboards.main_menu_keyboard import MainMenuKeyboard
from logger import get_logger

from handlers.template_handlers.message_handler_template import (
    MessageHandlerTemplate,
)
from settings.settings import config

router = Router()


@router.message(Text('Главная'))
@flags.rate_limit({config['FlagsNames']['throttling_key']: 'main_menu',
                   config['FlagsNames']['throttle_time']: 1})
@clear_inline_message
@will_delete_user_message
class MainMenuHandler(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info('in bot bot_id=%d user with username=%s '
                 'and chat_id=%d press "/Главная"',
                 self.bot.id, self.chat.username, self.chat.id)

        await self.clear_state()
        return await self.send_deleted_message(
            text='Главная',
            reply_markup=MainMenuKeyboard().get(),
        )
