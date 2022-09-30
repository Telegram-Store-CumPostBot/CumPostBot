from pydantic import BaseModel


class PaymentUser(BaseModel):
    id: int

    def get_payment_comment(self):
        return f'{self.id}'
