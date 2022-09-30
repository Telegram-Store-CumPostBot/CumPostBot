from typing import Optional

from glQiwiApi.core.abc.base_api_client import BaseAPIClient
from glQiwiApi.core.abc.base_api_client import RequestServiceFactoryType
from glQiwiApi.core.request_service import RequestServiceProto
from glQiwiApi.core.session import AiohttpSessionHolder
from glQiwiApi.utils.validators import PhoneNumber, String

from services.payment_services.QiWi.QiWiAPI.methods.abstract.\
    BaseQiWiMethod import BaseQiWiMethod
from services.payment_services.QiWi.QiWiAPI.request_service.\
    RequestService import CustomRequestService


class BaseQiWiClient(BaseAPIClient):
    _phone_number = PhoneNumber(maxsize=15, minsize=11, optional=True)
    _api_access_token = String(optional=False)

    def __init__(
        self,
        api_access_token: str,
        phone_number: Optional[str] = None,
        request_service_factory: Optional[RequestServiceFactoryType] = None,
    ) -> None:
        self._api_access_token = api_access_token
        self._phone_number = phone_number

        BaseAPIClient.__init__(self, request_service_factory)

    async def _create_request_service(self) -> RequestServiceProto:
        from glQiwiApi import __version__

        return CustomRequestService(
            access_token=self._api_access_token,
            session_holder=AiohttpSessionHolder(
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': f'Bearer {self._api_access_token}',
                    'Host': 'edge.qiwi.com',
                    'User-Agent': f'glQiwiApi/{__version__}',
                }
            )
        )

    @classmethod
    async def execute_method(cls, method: BaseQiWiMethod):
        return await method.build_method()
