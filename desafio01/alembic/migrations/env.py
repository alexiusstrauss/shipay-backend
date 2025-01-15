from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from alembic import context

# Importa a base e os modelos
from src.system.config import config as app_config
from src.database.models.base_model import ORMBaseModel
from src.database.models.customer_validation import ValidationRequestLogORM # NOQA

# Verifica se o DB_URL é sqlite para adicionar o aiosqlite
DB_URL = app_config.DATABASE_URL
if DB_URL.startswith("sqlite:///"):
    DB_URL = DB_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

# Carrega a configuração do arquivo alembic.ini
config = context.config
config.set_main_option('sqlalchemy.url', DB_URL)

# Interpreta o arquivo de configuração do alembic.ini
fileConfig(config.config_file_name)

# Definição do alvo da metadata para autogenerate
target_metadata = ORMBaseModel.metadata # NOQA

def run_migrations_offline():
    """Executa migrações no modo 'offline'.

    Isso configura o contexto apenas com uma URL
    e não um Engine. Ao pular a criação do Engine, não precisamos
    nem de um DBAPI disponível.

    Chamadas para context.execute() aqui emitem a string dada para a
    saída do script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: AsyncConnection):
    context.configure(
        connection=connection, # NOQA
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Executa migrações no modo 'online'.

    Neste cenário, precisamos criar um Engine
    e associar uma conexão com o contexto.
    """
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations) # NOQA

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())