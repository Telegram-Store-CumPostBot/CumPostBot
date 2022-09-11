from abc import abstractmethod

from errors.NoFoundKeys import NoFoundKeysError


class PaymentService:
    init_kwargs = ['key']

    def __init__(self, **kwargs):
        if not all([key in kwargs for key in self.init_kwargs]):
            raise NoFoundKeysError('kwargs', [key for key in self.init_kwargs if key not in kwargs])

    @abstractmethod
    def create_payroll(self, user: dict, ):
        pass

    @abstractmethod
    def __repr__(self):
        pass
