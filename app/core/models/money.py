from core.models.model import Model


class Money(Model):
    amount: str
    currency: str
