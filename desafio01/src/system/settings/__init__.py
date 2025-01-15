import os

from dotenv import load_dotenv

from .base import BaseSettings
from .dev import DevSettings
from .local import LocalSettings
from .prod import ProdSettings
from .test import TestSettings

load_dotenv()

env = os.getenv('ENVIRONMENT', 'local')

environment_map = {
    'local': LocalSettings,
    'dev': DevSettings,
    'prod': ProdSettings,
    'test': TestSettings,
}


def get_environment() -> BaseSettings:
    environment = environment_map.get(env, DevSettings)
    return environment()
