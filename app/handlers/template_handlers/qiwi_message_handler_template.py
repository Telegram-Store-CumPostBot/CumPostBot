from abc import ABC
from typing import Any

from aiogram import flags

from handlers.custom_base_handlers import CustomMessageHandler
from middlewares.middlewares_settings import ThrottlingSettings
from mixins.handler_mixins.FSMHandlerMixin import FSMHandlerMixin
from mixins.handler_mixins.UpdateBotMixin import UpdateBotMixin


@flags.rate_limit(ThrottlingSettings.DEFAULT_FLAGS)
class QiWiMessageHandlerTemplate(
    CustomMessageHandler,
    FSMHandlerMixin,
    UpdateBotMixin,
    ABC
):
    async def handle(self) -> Any:
        if not self.bot.has_qiwi:
            return
        await self.work()
