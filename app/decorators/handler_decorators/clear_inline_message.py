import asyncio

from aiogram.dispatcher.handler import BaseHandler

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
            self.__handler: CustomMessageHandler = cls(*args, **kwargs)

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
                return self.__handler.__getattribute__(item)
            else:
                self.__clear()
                return self.handle

        async def handle(self):
            await self.__clear()
            await self.__handler.handle()

        async def __clear(self):
            print('in clear')
            callbacks = self.__handler.data.get('clear_inline_messages')
            if not callbacks:
                return
            print('clearing')
            await asyncio.gather(*callbacks)
            self.__handler.data['clear_inline_messages'] = []

    return ClearInlineMessage
