from src.database import get_db
from src.packages.customer_validation.adapters.cnpj_service_adapter import (
    CNPJServiceAdapter,
)
from src.packages.customer_validation.adapters.fallback_cep_strategy import (
    FallbackCEPStrategy,
)
from src.packages.customer_validation.adapters.primary_cep_strategy import (
    PrimaryCEPStrategy,
)
from src.packages.customer_validation.controllers.customer_validation_controller import (
    CustomerValidationController,
)
from src.packages.customer_validation.repositories.customer_validation_repository import (
    CustomerValidationRepository,
)
from src.packages.customer_validation.services.cep_service import CEPService
from src.packages.customer_validation.services.validation_service import (
    ValidationService,
)
from src.system.config import config


def create_customer_validation_repository() -> CustomerValidationRepository:
    """
    Cria e retorna uma instância de CustomerValidationRepository.
    Passa a função `get_db` como session_factory.
    """
    return CustomerValidationRepository(session_factory=get_db)


def create_cep_service() -> CEPService:
    """
    Cria e retorna uma instância de CEPService com estratégias.
    """
    strategies = [
        PrimaryCEPStrategy(base_url=config.PRIMARY_CEP_API),
        FallbackCEPStrategy(base_url=config.FALLBACK_CEP_API),
    ]
    return CEPService(strategies)


def create_customer_validation_service() -> ValidationService:
    """
    Cria e retorna uma instância de ValidationService.
    """
    repository = create_customer_validation_repository()
    cnpj_service = CNPJServiceAdapter(base_url=config.CNPJ_API)
    cep_service = create_cep_service()
    return ValidationService(
        cnpj_service=cnpj_service,
        cep_service=cep_service,
        repository=repository,
    )


def create_customer_validation_controller() -> CustomerValidationController:
    """
    Cria e retorna uma instância de CustomerValidationController.
    """
    service = create_customer_validation_service()
    return CustomerValidationController(validation_service=service)
