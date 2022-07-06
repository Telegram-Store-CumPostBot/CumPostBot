from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.regular import MainMenuKeyboard
from logger import get_logger


async def start(message: Message, state: FSMContext):
    log = get_logger(__name__)
    if state and (current_state := await state.get_state()) is not None:
        log.debug(f"Canceling state: {current_state}")
        await state.finish()

    start_text = (
        "Welcome to the Bot!\n"
        "do you want me to get to know you better? "
        "press the let's start button bellow:"
    )
    return await message.answer(
        text=start_text,
        reply_markup=MainMenuKeyboard.get(),
    )


def register_base(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
