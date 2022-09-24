from abc import ABC
from aiogram import flags

from handlers.custom_base_handlers import CustomMessageHandler
from middlewares.middlewares_settings import ThrottlingSettings
from mixins.handler_mixins.FSMHandlerMixin import FSMHandlerMixin
from mixins.handler_mixins.QiWiWrapperMixin import QiWiWrapperMixin
from mixins.handler_mixins.UpdateBotMixin import UpdateBotMixin


@flags.rate_limit(ThrottlingSettings.DEFAULT_FLAGS)
class MessageHandlerTemplate(CustomMessageHandler, FSMHandlerMixin, UpdateBotMixin, ABC):
    pass


@flags.rate_limit(ThrottlingSettings.DEFAULT_FLAGS)
class QiWiMessageHandlerTemplate(CustomMessageHandler, FSMHandlerMixin, UpdateBotMixin, QiWiWrapperMixin, ABC):
    pass
