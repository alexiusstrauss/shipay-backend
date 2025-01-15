from enum import Enum


class StrEnum(str, Enum):
    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value


class EnvironmentSet(StrEnum):
    PRODUCTION = 'production'
    DEVELOPMENT = 'development'
    SANDBOX = 'sandbox'
    STAGING = 'staging'
    TESTING = 'testing'
