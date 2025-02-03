from infra.sqlalchemy.model import SaModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

_engine: AsyncEngine
_AsyncSessionLocal: async_sessionmaker[AsyncSession]


def init_rdb(url: str, debug: bool = True) -> None:
    global _engine
    _engine = create_async_engine(url, echo=debug)

    global _AsyncSessionLocal
    _AsyncSessionLocal = async_sessionmaker(
        bind=_engine,
        autocommit=False,
        autoflush=False,
    )


async def create_tables(tables: list[SaModel]) -> None:
    global _engine
    async with _engine.begin() as conn:
        for table in tables:
            await conn.run_sync(table.__table__.create, checkfirst=True)


def get_session_factory():
    global _AsyncSessionLocal
    factory = _AsyncSessionLocal
    return factory
