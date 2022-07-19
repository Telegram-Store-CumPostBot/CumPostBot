from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags.getter import get_flag
from aiogram.types import Message

from middlewares.middlewares_settings import ThrottlingSettings

from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    caches = {
        ThrottlingSettings.DEFAULT_THROTTLE_KEY: TTLCache(maxsize=10_000, ttl=ThrottlingSettings.DEFAULT_THROTTLE_TIME)
    }

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        throttling_flags = get_flag(data, 'rate_limit')
        if not throttling_flags:
            throttling_flags = ThrottlingSettings.DEFAULT_FLAGS

        throttling_key = throttling_flags['throttling_key']
        throttle_time = throttling_flags['throttle_time']

        if not f'{throttling_key}_{throttle_time}' in self.caches:
            self.caches[f'{throttling_key}_{throttle_time}'] = TTLCache(
                maxsize=ThrottlingSettings.MAX_CACHE_SIZE,
                ttl=throttle_time
            )

        if event.chat.id in self.caches[f'{throttling_key}_{throttle_time}']:
            return
        else:
            self.caches[f'{throttling_key}_{throttle_time}'][event.chat.id] = None

        return await handler(event, data)
