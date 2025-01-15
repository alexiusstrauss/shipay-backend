import pytest
from unittest.mock import AsyncMock
from src.packages.customer_validation.adapters.cnpj_service_adapter import CNPJServiceAdapter

@pytest.fixture
def cnpj_service():
    """Fixture para criar uma instância do CNPJServiceAdapter com uma URL fake."""
    return CNPJServiceAdapter(base_url="https://fake-cnpj-api.com")

