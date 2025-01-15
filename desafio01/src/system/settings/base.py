import os


class BaseSettings:
    def __init__(self):
        # Configurações gerais
        self.APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FASTAPI")
        # Configuração do banco de dados
        self.DATABASE_URL: str = self._get_database_url()

        # Configurações de api externas
        self.PRIMARY_CEP_API: str = os.getenv("PRIMARY_CEP_API", "https://brasilapi.com.br/api/cep/v2")
        self.FALLBACK_CEP_API: str = os.getenv("FALLBACK_CEP_API", "https://viacep.com.br/ws")
        self.CNPJ_API: str = os.getenv("CNPJ_API", "https://brasilapi.com.br/api/cnpj/v1")

    @staticmethod
    def _get_database_url() -> str:
        db_url = os.getenv("DATABASE_URL", "sqlite:///./src/local.db")
        if db_url.startswith("sqlite:///"):
            db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
        elif db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

        return db_url
