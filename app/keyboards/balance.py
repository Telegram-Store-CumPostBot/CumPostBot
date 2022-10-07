from aiogram.types import KeyboardButton

from keyboards.base import RegularKeyboard


class MainMenuKeyboard(RegularKeyboard):
    @property
    def _keyboard(self):
        return [
            [
                KeyboardButton(text='Пополнить'),
                KeyboardButton(text='Проверить пополнения')
            ],
            [
                KeyboardButton(text='Главная'),
                KeyboardButton(text='Назад')
            ],
        ]
