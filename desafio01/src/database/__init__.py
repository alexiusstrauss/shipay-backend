import asyncio
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# from src.database.models.base_model import ORMBaseModel
from src.system.config import config as app_config

# Detecta e ajusta o driver com base no banco de dados
DB_URL = app_config.DATABASE_URL

engine = create_async_engine(app_config.DATABASE_URL, pool_pre_ping=False, pool_recycle=3600, echo_pool=False)

# Configuração da fábrica de sessões
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)  # NOQA

# Atualização do tipo de ContextDBSession
ContextDBSession = Callable[[], AsyncContextManager[AsyncSession]]


# Gerenciamento da sessão de banco de dados
@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc
        finally:
            await session.close()
            await asyncio.shield(session.close())


# Definição da interface base para repositórios
class BaseRepositoryInterface:
    def __init__(self, session: ContextDBSession):
        self.session = session
