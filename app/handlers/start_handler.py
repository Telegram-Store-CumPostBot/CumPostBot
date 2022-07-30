from typing import Any

from aiogram import Router

from database.models.customer import Customer
from keyboards.main_menu_keyboard import MainMenuKeyboard
from logger import get_logger

from handlers.handlers_templates import MessageHandlerTemplate


router = Router()


@router.message(commands=['start'])
class StartHandler(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info(f'user with username={self.chat.username} and chat_id={self.chat.id} press "/start"')

        if self.state and (current_state := await self.state.get_state()) is not None:
            log.debug(f"Canceling state: {current_state}")
            await self.state.clear()

        start_text = f'{self.chat.first_name} {self.chat.last_name}, добро пожаловать в секту!)'

        if not await Customer.check_availability(self.chat.id):
            log.info(f'register new user with chat_id={self.chat.id} and username={self.chat.username}')
            await Customer.create_new(
                chat_id=self.chat.id,
                username=self.chat.username,
                first_name=self.chat.first_name,
                last_name=self.chat.last_name,
            )
            start_text = f'{self.chat.first_name} {self.chat.last_name}, добро пожаловать в секту!)'

        return await self.event.answer(
            text=start_text,
            reply_markup=MainMenuKeyboard().get(),
        )
