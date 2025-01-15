from abc import ABC, abstractmethod
from typing import List

from fastapi import BackgroundTasks

from src.packages.customer_validation.ports.cep_strategy_interface import CEPStrategyInterface
from src.packages.customer_validation.schemas.validation_schemas import (
    ValidationRequest,
    ValidationResponse,
)


class ValidationServiceInterface(ABC):
    """
    Interface para o serviço de validação de clientes.
    Define os métodos que devem ser implementados por ValidationService.
    """

    @abstractmethod
    async def validate(self, request: ValidationRequest, strategies: List[CEPStrategyInterface]) -> ValidationResponse:
        ...

    @abstractmethod
    async def retry_validation_task(self, cnpj: str, cep: str):
        """
        Realiza uma nova tentativa de validação em background.

        :param cnpj: CNPJ do cliente.
        :param cep: CEP do cliente.
        """
        ...

    @abstractmethod
    def schedule_retry(self, request: ValidationRequest, background_tasks: BackgroundTasks):
        """
        Agenda uma nova tentativa de validação para execução em background.
        :param request: ValidationRequest com os dados do cliente.
        :param background_tasks: Objeto de tarefas em background.
        """
        ...
