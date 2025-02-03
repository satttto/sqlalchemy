from auth.domain.adapters.company_repository import CompanyRepository
from auth.domain.models.company import Company
from auth.infra.sqlalchemy.company import SaCompany
from auth.infra.sqlalchemy.user import SaUser
from infra.sqlalchemy.repository import SaRepository
from infra.sqlalchemy.transaction_manager import SaTransactionManager
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class SaCompanyRepository(CompanyRepository, SaRepository[Company, SaCompany]):
    sqlalchemy_model_class = SaCompany

    def __init__(self, transaction_manager: SaTransactionManager):
        self._tx_manager = transaction_manager

    async def create(self, model: Company) -> None:
        await self._create(model)

    async def update(self, model: Company) -> None:
        await self._update(model)

    async def list_companies(self) -> list[Company]:
        stmt = select(SaCompany).options(
            joinedload(SaCompany.employees).joinedload(SaUser.addresses)
        )
        result = await self._execute_stmt(stmt)
        return self._get_all(result)
