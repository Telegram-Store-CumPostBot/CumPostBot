from abc import abstractmethod


class Payroll:
    def __init__(self):
        pass

    @abstractmethod
    def payment_info(self):
        pass

    @property
    @abstractmethod
    async def user_info(self):
        pass

    @abstractmethod
    async def cancel(self):
        pass

    @abstractmethod
    async def check_payment(self):
        pass
