import asyncio

from aiogram.handlers import BaseHandler

from handlers.custom_base_handlers import CustomMessageHandler


def clear_inline_message(cls):
    """Декоратор над хендлером, который вызывает все колбеки из
    хранилища диалога с пользователем под ключем 'clear_inline_messages'"""
    # наследуемся от BaseHandler для того, чтобы проходила проверка
    # aiogram.event.handler.HandlerObject.__post_init__ {
    #   if inspect.isclass(callback) and issubclass(callback, BaseHandler)
    # }
    # иначе не работает почему-то(((
    # BaseHandler.init скипнул за ненадобностью
    # handle нужно определить, чтобы ABC не ругался
    class ClearInlineMessage(BaseHandler):
        def __init__(self, *args, **kwargs):
            self._handler: CustomMessageHandler = cls(*args, **kwargs)

        def __getattribute__(self, item):
            # метод этого класса или нет
            try:
                x = super().__getattribute__(item)
            except AttributeError:
                pass
            else:
                return x

            # если просят handle, то оборачиваем его,
            # иначе просто возвращаем метод декорируемого хендлера
            if item != 'handle':
                return self._handler.__getattribute__(item)
            else:
                print('gay')
                self._clear()
                return self.handle

        async def handle(self):
            await self._clear()
            await self._handler.handle()

        async def _clear(self):
            bot = self._handler.bot
            user_id = self._handler.from_user.id
            messages = bot.get_deleted_message(user_id)
            if not messages:
                return
            tasks = [bot.delete_message(chat_id, message_id)
                     for chat_id, message_id in messages]
            await asyncio.gather(*tasks)
            bot.clear_deleted_message(user_id)

    return ClearInlineMessage
