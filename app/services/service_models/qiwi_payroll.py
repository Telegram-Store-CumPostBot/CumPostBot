from services.service_models.abstract.payroll import Payroll


class QiWiPayroll(Payroll):
    def payment_info(self):
        pass

    async def user_info(self):
        pass

    async def cancel(self):
        pass

    async def check_payment(self):
        pass
