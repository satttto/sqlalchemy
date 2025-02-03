from auth.domain.models.user import User
from auth.infra.sqlalchemy.address import SaAddress
from infra.sqlalchemy.model import SaModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class SaUser(SaModel):
    model_class = User

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    addresses: Mapped[list["SaAddress"]] = relationship("SaAddress")
