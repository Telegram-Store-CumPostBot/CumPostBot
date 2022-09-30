from abc import abstractmethod


class PaymentService:
    @abstractmethod
    async def check_new_payments(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
