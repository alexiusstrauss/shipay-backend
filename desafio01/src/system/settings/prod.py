import os

from .base import BaseSettings


class ProdSettings(BaseSettings):
    def __init__(self):
        super().__init__()
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "PRODUCAO-API")
        self.DATABASE_URL: str = self._get_database_url()
