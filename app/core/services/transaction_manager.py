from abc import ABC
from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncIterator


class TransactionManager(ABC):
    @abstractmethod
    @asynccontextmanager
    async def start_transaction(self) -> AsyncIterator[None]:
        yield

    @abstractmethod
    async def begin(self) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
