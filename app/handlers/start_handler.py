from typing import Any

from aiogram import Router

from database.models.customer import Customer
from keyboards.main_menu_keyboard import MainMenuKeyboard
from logger import get_logger

from handlers.handlers_templates import MessageHandlerTemplate
from middlewares.middlewares_settings import ThrottlingSettings


router = Router()


@router.message(commands=['start'])
class StartHandler(MessageHandlerTemplate):
    def handle_flags(self):
        return ThrottlingSettings.DEFAULT_FLAGS

    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info(f'user with username={self.chat.username} and chat_id={self.chat.id} press "/start"')

        if self.state and (current_state := await self.state.get_state()) is not None:
            log.debug(f"Canceling state: {current_state}")
            await self.state.clear()

        start_text = f'И снова здравствуй дед максим ({self.chat.first_name} {self.chat.last_name})'

        # использую без limit, чтобы сразу отловить наличие более одной копии и пофиксить такой трабл
        # user = await Customer.objects.filter(chat_id=self.chat.id).limit(1).values('id')
        user = await Customer.objects.filter(chat_id=self.chat.id).values('id')
        assert len(user) in (0, 1)

        if not user:
            log.info(f'register new user with chat_id={self.chat.id} and username={self.chat.username}')
            await Customer(
                chat_id=self.chat.id,
                username=self.chat.username,
                first_name=self.chat.first_name,
                last_name=self.chat.last_name,
            ).save()
            start_text = f'И снова здравствуй дед максим ({self.chat.first_name} {self.chat.last_name})'

        return await self.event.answer(
            text=start_text,
            reply_markup=MainMenuKeyboard().get(),
        )
