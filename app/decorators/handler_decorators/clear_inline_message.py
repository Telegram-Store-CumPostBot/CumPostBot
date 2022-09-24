from handlers.custom_base_handlers import CustomMessageHandler


def clear_inline_message(cls):
    class ClearInlineMessage:
        def __init__(self, *args, **kwargs):
            self.__handler: CustomMessageHandler = cls(*args, **kwargs)

        def __getattribute__(self, item):
            if item != 'handle':
                return self.__get_attr_subclass(item)

            return self.__custom_handle()

        def __get_attr_subclass(self, item):
            return self.__handler.__getattribute__(item)

        def __custom_handle(self):
            print('gay')
            callbacks = self.__handler.data['clear_inline_messages']
            for clear in callbacks:
                clear()

            return self.__handler.handle

    return ClearInlineMessage
