from contextlib import asynccontextmanager
from typing import AsyncGenerator

from core.services.transaction_manager import TransactionManager


class CompositeTransactionManager(TransactionManager):
    def __init__(self, transaction_managers: list[TransactionManager]):
        self.tx_managers = transaction_managers

    @asynccontextmanager
    async def start_transaction(self) -> AsyncGenerator[None, None]:
        try:
            await self.begin()
            yield
            await self.commit()
        except Exception as e:
            print(e)
            await self.rollback()
        finally:
            await self.close()

    async def begin(self) -> None:
        for tx_manager in self.tx_managers:
            await tx_manager.begin()

    async def commit(self) -> None:
        for manager in self.tx_managers:
            await manager.commit()

    async def rollback(self) -> None:
        for manager in self.tx_managers:
            await manager.rollback()

    async def close(self) -> None:
        for manager in self.tx_managers:
            await manager.close()
