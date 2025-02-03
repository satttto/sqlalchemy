from typing import Any
from typing import Callable

from auth.domain.models.company import Company
from auth.infra.sqlalchemy.user import SaUser
from core.models.money import Money
from infra.sqlalchemy.model import SaModel
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class SaCompany(SaModel):
    model_class = Company

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fund_amount: Mapped[str]
    fund_currency: Mapped[str]
    employees: Mapped[list["SaUser"]] = relationship("SaUser")

    some_field: Mapped[str]

    def _to_model_custom_converters(self) -> dict[str, Callable[[], Any]]:
        def f() -> Money:
            fund_amount: str = self.fund_amount
            fund_currency: str = self.fund_currency
            return Money(amount=fund_amount, currency=fund_currency)

        def f2() -> str:
            return self.some_field

        return {"fund": f, "_some_hidden_field": f2}

    @classmethod
    def _from_model_custom_converters(
        cls,
    ) -> dict[str, Callable[[SaModel, Any], None]]:
        def f(sa_model: SaModel, money: Money) -> None:
            setattr(sa_model, "fund_amount", money.amount)
            setattr(sa_model, "fund_currency", money.currency)

        def f2(sa_model: SaModel, value: str) -> None:
            print(value)
            setattr(sa_model, "some_field", value)

        return {"fund": f, "_some_hidden_field": f2}
