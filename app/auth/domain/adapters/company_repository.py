from abc import ABC
from abc import abstractmethod

from auth.domain.models.company import Company


class CompanyRepository(ABC):
    @abstractmethod
    async def create(self, company: Company) -> None:
        pass

    @abstractmethod
    async def update(self, company: Company) -> None:
        pass

    @abstractmethod
    async def list_companies(self) -> list[Company]:
        pass
