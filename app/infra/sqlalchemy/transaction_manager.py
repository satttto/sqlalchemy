from contextlib import asynccontextmanager
from typing import AsyncGenerator

from core.services.transaction_manager import TransactionManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


class SaTransactionManager(TransactionManager):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
        self.is_in_transaction = False
        self._session: AsyncSession | None = None

    async def get_session(self) -> AsyncSession:
        if not self.is_in_transaction or self._session is None:
            raise RuntimeError(
                "No active transaction. Use 'start_transaction' context manager."
            )
        return self._session

    @asynccontextmanager
    async def start_transaction(self) -> AsyncGenerator[None, None]:
        print("......Starting tx.....")
        try:
            await self.begin()
            print("########### BEGAN..")
            yield
            await self.commit()
        except Exception as e:
            print(e)
            print("########### Rolling back....")
            await self.rollback()
        finally:
            await self.close()
        print("......Closing tx.....")

    async def begin(self) -> None:
        self._session = self.session_factory()
        await self._session.begin()
        self.is_in_transaction = True

    async def commit(self) -> None:
        if self._session is not None and self.is_in_transaction is True:
            await self._session.commit()
        self.is_in_transaction = False

    async def rollback(self) -> None:
        if self._session is not None and self.is_in_transaction is True:
            await self._session.rollback()
        self.is_in_transaction = False

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
