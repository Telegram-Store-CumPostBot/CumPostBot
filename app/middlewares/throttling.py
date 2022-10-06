from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message

from errors.NoFoundRateLimitFlag import NoFoundRateLimitFlagError
from logger import get_logger
from middlewares.middlewares_settings import ThrottlingSettings

from cachetools import TTLCache

from settings.settings import config


class ThrottlingMiddleware(BaseMiddleware):
    caches = {}
    throttling_key = config['FlagsNames']['throttling_key']
    throttle_time = config['FlagsNames']['throttle_time']

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

        throttle_key = throttling_flags[self.throttling_key]
        throttle_time = throttling_flags[self.throttle_time]
        throttle_pattern = f'{throttle_key}_{throttle_time}'

        if throttle_pattern not in self.caches:
            self.caches[throttle_pattern] = TTLCache(
                maxsize=ThrottlingSettings.MAX_CACHE_SIZE,
                ttl=throttle_time
            )

        if event.chat.id in self.caches[throttle_pattern]:
            log.info(f'Drop message by {event.chat.id}-{event.chat.username}')
            await event.delete()
            return
        else:
            self.caches[throttle_pattern][event.chat.id] = None
        return await handler(event, data)
