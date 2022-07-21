from typing import Any

from aiogram import Router

from keyboards.regular import MainMenuKeyboard
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
        if self.state and (current_state := await self.state.get_state()) is not None:
            log.debug(f"Canceling state: {current_state}")
            await self.state.clear()

        start_text = (
            "Welcome to the Bot!\n"
            "do you want me to get to know you better? "
            "press the let's start button bellow:"
        )
        return await self.event.answer(
            text=start_text,
            reply_markup=MainMenuKeyboard.get(),
        )
