from aiogram.dispatcher.handler import BaseHandler

from handlers.custom_base_handlers import CustomMessageHandler


def clear_inline_message(cls):
    class ClearInlineMessage(BaseHandler):
        def __init__(self, *args, **kwargs):
            self.__handler: CustomMessageHandler = cls(*args, **kwargs)

        def __getattribute__(self, item):
            print(f'{item=}')
            print('start get attribute')
            # метод этого класса или нет
            try:
                x = super().__getattribute__(item)
            except AttributeError:
                print('метод не из этого класса')
                pass
            else:
                print('метод из этого класса')
                print(f'{x=}')
                return x

            # если просят handle, то оборачиваем его,
            # иначе просто возвращаем метод декорируемого хендлера
            if item != 'handle':
                print('attribute in`t handle')
                attr = self.__handler.__getattribute__(item)
                print(f'{attr=}')
                return attr
            else:
                print('attribute is handle')
                self.__clear()
                return self.__new_handle

        def __get_attr_subclass(self, item):
            attr = self.__handler.__getattribute__(item)
            print(f'{attr=}')
            return attr

        async def handle(self):
            print('new handle')
            await self.__clear()
            await self.__handler.handle()

        async def __clear(self):
            print('clear message')
            callbacks = self.__handler.data.get('clear_inline_messages')
            if not callbacks:
                print('not callbacks')
                return

            print('await callbacks')
            for clear in callbacks:
                await clear()

    return ClearInlineMessage
