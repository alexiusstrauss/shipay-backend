import os

from .base import BaseSettings


class TestSettings(BaseSettings):
    def __init__(self):
        super().__init__()
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "TESTING-API")
        self.DATABASE_URL: str = self._get_database_url_for_testing()

    @staticmethod
    def _get_database_url_for_testing() -> str:
        db_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
        if db_url.startswith("sqlite:///"):
            db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
        return db_url
