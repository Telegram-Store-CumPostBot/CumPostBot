from aiogram.types import KeyboardButton

from keyboards.base import RegularKeyboard
from settings.message_constants import PROFILE


class MainMenuKeyboard(RegularKeyboard):
    @property
    def _keyboard(self):
        return [
            [
                KeyboardButton(text='Купить товар'),
                KeyboardButton(text='Наличие товара')
            ],
            [
                KeyboardButton(text=PROFILE),
                KeyboardButton(text='Баланс')
            ],
            [
                KeyboardButton(text='Помощь'),
                KeyboardButton(text='Межботные функции')
            ],
        ]
