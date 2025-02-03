from core.models.model import Model


class Address(Model):
    id: int
    postal_code: str
    user_id: int
