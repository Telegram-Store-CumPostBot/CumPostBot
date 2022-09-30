from typing import Any

from aiogram import Router

from database.models.api.customer import DBAPICustomer
from keyboards.main_menu_keyboard import MainMenuKeyboard
from logger import get_logger

from handlers.template_handlers.message_handler_template import (
    MessageHandlerTemplate,
)


router = Router()


@router.message(commands=['start'])
class StartHandler(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info('in bot bot_id=%d user with username=%s '
                 'and chat_id=%d press "/start"',
                 self.bot.id, self.chat.username, self.chat.id)
        await self.clear_state()

        name = f'{self.chat.first_name} {self.chat.last_name}'
        start_text = f'И снова здравствуй дед максим ({name})'

        if not await DBAPICustomer.check_availability(
                self.chat.id,
                self.bot.id
        ):
            log.info('bot_id=%d, chat_id=%d, username=%s: register new user ',
                     self.bot.id, self.chat.id, self.chat.username)
            await DBAPICustomer.create_user(
                chat_id=self.chat.id,
                tg_bot_id=self.bot.id,
                username=self.chat.username,
                first_name=self.chat.first_name,
                last_name=self.chat.last_name,
            )
            start_text = f'{name}, добро пожаловать в секту!)'

        return await self.event.answer(
            text=start_text,
            reply_markup=MainMenuKeyboard().get(),
        )
