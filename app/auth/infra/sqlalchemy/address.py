from auth.domain.models.address import Address
from infra.sqlalchemy.model import SaModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class SaAddress(SaModel):
    model_class = Address

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    postal_code: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
