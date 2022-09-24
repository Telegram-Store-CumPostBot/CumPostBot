from handlers.custom_base_handlers import CustomMessageHandler


def clear_inline_message(cls):
    class ClearInlineMessage:
        def __init__(self, *args, **kwargs):
            self.__handler: CustomMessageHandler = cls(*args, **kwargs)

        def __getattribute__(self, item):
            print(f'{item=}')
            print('start get attribute')
            # метод этого класса или нет
            try:
                x = self.__getattribute__(item)
            except AttributeError:
                pass
            else:
                return x

            # если просят handle, то оборачиваем его,
            # иначе просто возвращаем метод декорируемого хендлера
            if item != 'handle':
                print('attribute in`t handle')
                return self.__get_attr_subclass(item)
            else:
                print('attribute is handle')
                self.__clear()
                return self.__new_handle

        def __get_attr_subclass(self, item):
            return self.__handler.__getattribute__(item)

        async def __new_handle(self):
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
