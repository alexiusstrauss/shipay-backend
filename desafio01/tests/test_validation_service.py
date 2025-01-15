import pytest
from unittest.mock import AsyncMock, MagicMock
from src.packages.customer_validation.schemas.validation_schemas import (
    ValidationRequest,
    ValidationResponse,
)
from src.packages.customer_validation.services.validation_service import ValidationService
from src.packages.customer_validation.ports.cep_strategy_interface import CEPStrategyInterface


@pytest.fixture
def mock_cnpj_service():
    cnpj_service = AsyncMock()
    cnpj_service.get_company_info = AsyncMock(return_value={
        "uf": "SP",
        "municipio": "São Paulo",
        "logradouro": "Rua Teste"
    })
    return cnpj_service


@pytest.fixture
def mock_repository():
    repository = AsyncMock()
    repository.save = AsyncMock()
    return repository


@pytest.fixture
def mock_strategy():
    strategy = MagicMock(spec=CEPStrategyInterface)
    strategy.get_address_info = AsyncMock(return_value={
        "state": "SP",
        "city": "São Paulo",
        "street": "Rua Teste"
    })
    strategy.map_address_info = MagicMock(return_value={
        "state": "SP",
        "city": "São Paulo",
        "street": "Rua Teste"
    })
    return strategy


@pytest.fixture
def mock_cep_service(mock_strategy):
    cep_service = MagicMock()
    cep_service.strategies = [mock_strategy]
    return cep_service


@pytest.fixture
def validation_service(mock_cnpj_service, mock_cep_service, mock_repository):
    return ValidationService(
        cnpj_service=mock_cnpj_service,
        cep_service=mock_cep_service,
        repository=mock_repository
    )


@pytest.mark.asyncio
async def test_validate_success(validation_service, mock_strategy):
    request = ValidationRequest(cnpj="12345678000195", cep="01001000")

    response = await validation_service.validate(request, [mock_strategy])

    assert response == ValidationResponse(valid=True, message="Validation successful")
    validation_service.repository.save.assert_called_once()



@pytest.mark.asyncio
async def test_retry_validation_task_success(validation_service, mock_strategy):
    request = ValidationRequest(cnpj="12345678000195", cep="01001000")

    response = await validation_service.retry_validation_task(request)

    assert response == ValidationResponse(valid=True, message="Validation successful")
    validation_service.repository.save.assert_called_once()

