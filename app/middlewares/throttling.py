from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags.getter import get_flag
from aiogram.types import Message

from errors.NoFoundRateLimitFlag import NoFoundRateLimitFlagError
from logger import get_logger
from middlewares.middlewares_settings import ThrottlingSettings

from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    caches = {}

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        log = get_logger(__name__)

        throttling_flags = get_flag(data, 'rate_limit')
        if not throttling_flags:
            raise NoFoundRateLimitFlagError()

        throttling_key = throttling_flags['throttling_key']
        throttle_time = throttling_flags['throttle_time']

        if f'{throttling_key}_{throttle_time}' not in self.caches:
            self.caches[f'{throttling_key}_{throttle_time}'] = TTLCache(
                maxsize=ThrottlingSettings.MAX_CACHE_SIZE,
                ttl=throttle_time
            )

        if event.chat.id in self.caches[f'{throttling_key}_{throttle_time}']:
            log.info(f'Drop message by {event.chat.id}-{event.chat.username}')
            return
        else:
            self.caches[f'{throttling_key}_{throttle_time}'][event.chat.id] = None

        return await handler(event, data)
