import os

from .base import BaseSettings


class LocalSettings(BaseSettings):
    def __init__(self):
        super().__init__()
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "DEVELOPMENT-API-local")
        self.DATABASE_URL: str = self._get_database_url()
