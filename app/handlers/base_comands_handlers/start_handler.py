from typing import Any

from aiogram import Router

from database.models.customer import Customer
from keyboards.main_menu_keyboard import MainMenuKeyboard
from logger import get_logger

from handlers.template_handlers.message_handler_template import MessageHandlerTemplate


router = Router()


@router.message(commands=['start'])
class StartHandler(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info('in bot bot_id=%d user with username=%s and chat_id=%d press "/start"', self.bot.id, self.chat.username, self.chat.id)

        if self.state and (current_state := await self.state.get_state()) is not None:
            log.debug('in bot_id=%d user with username=%s and chat_id=%d: canceling state: %s', self.bot.id, self.chat.username, self.chat.id,
                      current_state)
            await self.state.clear()

        start_text = f'И снова здравствуй дед максим ({self.chat.first_name} {self.chat.last_name})'

        if not await Customer.check_availability(self.chat.id, self.bot.id):
            log.info('in bot_id=%d register new user with chat_id=%d and username=%s', self.bot.id, self.chat.id, self.chat.username)
            await Customer.create_new(
                chat_id=self.chat.id,
                bot_id=self.bot.id,
                username=self.chat.username,
                first_name=self.chat.first_name,
                last_name=self.chat.last_name,
            )
            start_text = f'{self.chat.first_name} {self.chat.last_name}, добро пожаловать в секту!)'

        return await self.event.answer(
            text=start_text,
            reply_markup=MainMenuKeyboard().get(),
        )
