from abc import abstractmethod

from data_models.user_notify import UserNotifications


class PaymentService:
    @abstractmethod
    async def check_new_payments(self) -> UserNotifications:
        pass

    @abstractmethod
    def __repr__(self):
        pass
