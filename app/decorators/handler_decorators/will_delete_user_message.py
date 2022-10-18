from aiogram.handlers import BaseHandler

from handlers.custom_base_handlers import CustomMessageHandler


def will_delete_user_message(cls):
    class WillDeleteUserMessage(BaseHandler):
        def __init__(self, *args, **kwargs):
            self._handler: CustomMessageHandler = cls(*args, **kwargs)
            self._handler._middleware.append(self.delete_user_message())

        async def delete_user_message(self):
            self._handler.bot.add_deleted_message(
                self._handler.event.chat.id,
                self._handler.event.message_id
            )

        def __getattribute__(self, item):
            # метод этого класса или нет
            try:
                x = super().__getattribute__(item)
            except AttributeError:
                pass
            else:
                return x

            if item != 'handle':
                return self._handler.__getattribute__(item)
            else:
                return self.handle
            # если просят handle, то оборачиваем его,
            # иначе просто возвращаем метод декорируемого хендлера
            return self._handler.__getattribute__(item)

        async def handle(self):
            await self._handler.handle()

    return WillDeleteUserMessage
