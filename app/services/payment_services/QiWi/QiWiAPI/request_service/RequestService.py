import asyncio
import time
from typing import TypeVar, Any, Optional

from glQiwiApi.core import RequestService
from glQiwiApi.core.abc.api_method import APIMethod
from glQiwiApi.core.session import AbstractSessionHolder

from settings.digit_constants import MAX_QIWI_REQUESTS_PER_SECOND

T = TypeVar('T')


class CustomRequestService(RequestService):
    last_execute = {}

    def __init__(
        self,
        access_token: str,
        session_holder: Optional[AbstractSessionHolder[Any]] = None,
    ) -> None:
        self._access_token = access_token
        self.last_execute[access_token] = 0
        super().__init__(session_holder)

    async def execute_api_method(
            self,
            method: APIMethod[T],
            **url_kw: Any
    ) -> T:
        while not self._can_execute_method:
            delay = time.time() - self.last_execute[self._access_token]
            await asyncio.sleep(MAX_QIWI_REQUESTS_PER_SECOND - delay)
        self.__class__.last_execute[self._access_token] = time.time()
        return await super().execute_api_method(method, **url_kw)

    @property
    def _can_execute_method(self) -> bool:
        delay = time.time() - self.last_execute[self._access_token]
        return not delay < MAX_QIWI_REQUESTS_PER_SECOND
