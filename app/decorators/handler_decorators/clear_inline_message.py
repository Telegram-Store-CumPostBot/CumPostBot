from handlers.custom_base_handlers import CustomMessageHandler


def clear_inline_message(cls):
    class ClearInlineMessage:
        def __init__(self, *args, **kwargs):
            self.__handler: CustomMessageHandler = cls(*args, **kwargs)

        def __getattribute__(self, item):
            if item != 'handle':
                return self.__get_attr_subclass(item)
            else:
                self.__clear()
                return self.__handler.handle

        def __get_attr_subclass(self, item):
            return self.__handler.__getattribute__(item)

        def __clear(self):
            print('gay')
            callbacks = self.__handler.data.get('clear_inline_messages')
            if not callbacks:
                return

            for clear in callbacks:
                clear()

    return ClearInlineMessage
