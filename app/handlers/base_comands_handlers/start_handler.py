from typing import Any

from aiogram import Router
from aiogram.filters import CommandStart

from database.engine import async_session, AsyncSessionTyping
from database.models.api.customer import DBAPICustomer
from keyboards.main_menu_keyboard import MainMenuKeyboard
from logger import get_logger

from handlers.template_handlers.message_handler_template import (
    MessageHandlerTemplate,
)


router = Router()


@router.message(CommandStart())
class StartHandler(MessageHandlerTemplate):
    async def work(self) -> Any:
        log = get_logger(__name__)
        log.info('in bot bot_id=%d user with username=%s '
                 'and chat_id=%d press "/start"',
                 self.bot.id, self.chat.username, self.chat.id)
        name = f'{self.chat.first_name} {self.chat.last_name}'
        start_text = f'И снова здравствуй дед максим ({name})'

        await self.clear_state()
        async with async_session() as session:
            if not await self._check_availability(session):
                start_text = f'{name}, добро пожаловать в секту!)'
                await self._create_user(session)
                await session.commit()

        return await self.event.answer(
            text=start_text,
            reply_markup=MainMenuKeyboard().get(),
        )

    async def _check_availability(self, session: AsyncSessionTyping) -> bool:
        return await DBAPICustomer.check_availability(
            session,
            self.chat.id,
            self.bot.id
        )

    async def _create_user(self, session: AsyncSessionTyping):
        log = get_logger(__name__)
        log.info(
            'bot_id=%d, chat_id=%d, username=%s: register new user',
            self.bot.id, self.chat.id, self.chat.username)
        await DBAPICustomer.create_user(
            session=session,
            chat_id=self.chat.id,
            username=self.from_user.username,
            first_name=self.from_user.first_name,
            last_name=self.chat.last_name,
            tg_bot_id=self.bot.id,
        )
