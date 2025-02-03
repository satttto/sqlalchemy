from typing import Generic
from typing import Sequence
from typing import Type
from typing import TypeVar

from core.models.model import Model
from infra.sqlalchemy.model import SaModel
from infra.sqlalchemy.transaction_manager import SaTransactionManager
from sqlalchemy import Result
from sqlalchemy import Select

ModelType = TypeVar("ModelType", bound="Model")
SaModelType = TypeVar("SaModelType", bound="SaModel")


class SaRepository(Generic[ModelType, SaModelType]):
    sqlalchemy_model_class: Type[SaModelType]

    def __init__(self, transaction_manager: SaTransactionManager):
        self._tx_manager = transaction_manager

    def get_transaction_manager_type(self) -> Type[SaTransactionManager]:
        return type(self._tx_manager)

    async def _create(self, model: ModelType) -> None:
        sa_model = self.sqlalchemy_model_class.from_model(model)

        if self._tx_manager.is_in_transaction:
            session = await self._tx_manager.get_session()
            session.add(sa_model)
        else:
            async with self._tx_manager.start_transaction():
                session = await self._tx_manager.get_session()
                session.add(sa_model)

    async def _update(self, model: ModelType) -> None:
        sa_model = self.sqlalchemy_model_class.from_model(model)

        if self._tx_manager.is_in_transaction:
            session = await self._tx_manager.get_session()
            await session.merge(sa_model)
        else:
            async with self._tx_manager.start_transaction():
                session = await self._tx_manager.get_session()
                await session.merge(sa_model)

    async def _execute_stmt(self, stmt: Select) -> Result:
        if self._tx_manager.is_in_transaction:
            print("---------- inside transaction")
            session = await self._tx_manager.get_session()
            result = await session.execute(stmt)
        else:
            print("---------- outside transaction")
            async with self._tx_manager.session_factory() as session:
                result = await session.execute(stmt)
        return result

    def _get_first_or_raise(self, result: Result, exception: Exception) -> ModelType:
        entity = result.scalars().first()
        if entity is None:
            raise exception
        return entity

    def _get_all(self, result: Result) -> list[ModelType]:
        seq: Sequence[SaModelType] = result.unique().scalars().all()
        return [item.to_model() for item in seq]
