
from auth.domain.adapters.company_repository import CompanyRepository
from auth.infra.sqlalchemy.company_repository import SaCompanyRepository
from core.services.composite_transaction_manager import CompositeTransactionManager
from core.services.transaction_manager import TransactionManager
from infra.sqlalchemy.db import get_session_factory
from infra.sqlalchemy.transaction_manager import SaTransactionManager


class Infra:
    def __init__(self):
        self.sa_tx_manager = None

    def get_transaction_manager(
        self, transaction_managers: list[TransactionManager]
    ) -> CompositeTransactionManager:
        return CompositeTransactionManager(transaction_managers)

    def get_sa_transaction_manager(self) -> SaTransactionManager:
        if self.sa_tx_manager is None:
            self.sa_tx_manager = SaTransactionManager(get_session_factory())
        return self.sa_tx_manager

    def get_company_repository(self) -> CompanyRepository:
        return SaCompanyRepository(self.get_sa_transaction_manager())
