from .settings import get_environment

settings = get_environment()


class Config:
    PROJECT_NAME = settings.PROJECT_NAME
    DATABASE_URL = settings.DATABASE_URL
    PRIMARY_CEP_API = settings.PRIMARY_CEP_API
    FALLBACK_CEP_API = settings.FALLBACK_CEP_API
    CNPJ_API = settings.CNPJ_API


config = settings
