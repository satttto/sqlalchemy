from auth.domain.models.user import User
from core.models.model import Model
from core.models.money import Money
from pydantic import PrivateAttr


class Company(Model):
    id: int
    name: str
    fund: Money
    _employees: list[User] = PrivateAttr(default_factory=list)
    _some_hidden_field: str = PrivateAttr(default="Satoshi")

    def add_employee(self, employee: User) -> None:
        self._employees.append(employee)

    @property
    def employees(self) -> list[User]:
        return self._employees

    @property
    def some_hidden_field(self) -> str:
        return self._some_hidden_field
