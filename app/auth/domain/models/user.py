from auth.domain.models.address import Address
from core.models.model import Model
from pydantic import PrivateAttr


class User(Model):
    id: int
    name: str
    company_id: int
    _addresses: list[Address] = PrivateAttr(default_factory=list)

    def add_address(self, address: Address) -> None:
        self._addresses.append(address)

    @property
    def addresses(self) -> list[Address]:
        return self._addresses
