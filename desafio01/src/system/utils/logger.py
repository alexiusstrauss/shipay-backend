import logging
import logging.config
import os
from logging import Logger

from src.system.enums import EnvironmentSet

ENVIRONMENT = os.getenv('ENVIRONMENT', default=EnvironmentSet.DEVELOPMENT)
LOG_LEVEL = os.getenv('LOG_LEVEL', default=logging.INFO)


def get_logger():
    return BaseLogger()


class WrappedLogger:
    """
    Wraps the Python logging module's logger object to ensure that all
    logging happens with the correct configuration as well as any extra
    information that might be required by the log file (for example, the user
    on the machine, hostname, IP address lookup, etc.).

    Subclasses must specify their logger as a class variable so all instances
    have access to the same logging object. Basic Usage:
    """

    logger: Logger
    log_format = '%(asctime)s  %(name)s  %(levelname)s - %(message)s'
    log_level = LOG_LEVEL

    def __init__(self, **kwargs):
        self.logger = kwargs.pop('logger', self.logger)
        self.log_level = kwargs.pop('log_level', self.log_level)
        self.log_format = kwargs.pop('log_format', self.log_format)

        if not self.logger or not hasattr(self.logger, 'log'):
            raise TypeError(f'Subclasses must specify a logger, not {type(self.logger)}')

        self.initialize()
        self.extras = kwargs

    def initialize(self):
        if len(self.logger.handlers) == 0:
            self.logger.propagate = False
            self.logger.setLevel(self.log_level)

            ch = logging.StreamHandler()
            formatter = logging.Formatter(self.log_format)
            ch.setFormatter(formatter)

            self.logger.addHandler(ch)

    def log(self, level, message, *args, **kwargs):
        """
        This is the primary method to override to ensure logging with extra
        options gets correctly specified.
        """
        extra = self.extras.copy()
        extra.update(kwargs.pop('datails', {}))

        if extra:
            message = f'{message} - {extra}'
        self.logger.log(level, message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        return self.log(logging.DEBUG, message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        return self.log(logging.INFO, message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        return self.log(logging.WARNING, message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        return self.log(logging.ERROR, message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        return self.log(logging.CRITICAL, message, *args, **kwargs)


class BaseLogger(WrappedLogger):
    """
    Usage:
        >>> logger = BaseLogger()
        >>> logger.info("You were here!")

    This will correctly log to the base logging handlers as well as provide
    extra information about the user who is logging via getpass.
    """

    logger = logging.getLogger(__name__)
