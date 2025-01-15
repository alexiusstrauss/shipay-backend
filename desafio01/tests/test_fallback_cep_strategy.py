import pytest
from unittest.mock import AsyncMock
from src.packages.customer_validation.adapters.fallback_cep_strategy import FallbackCEPStrategy

@pytest.fixture
def fallback_strategy():
    """Instância da estratégia FallbackCEPStrategy."""
    return FallbackCEPStrategy(base_url="https://fake-api.com")


def test_map_address_info(fallback_strategy):
    """Teste para verificar o mapeamento das informações do endereço."""
    input_data = {
        "uf": "SP",
        "localidade": "São Paulo",
        "logradouro": "Avenida Brigadeiro Faria Lima"
    }
    expected_output = {
        "state": "SP",
        "city": "SAO PAULO",
        "street": "Avenida Brigadeiro Faria Lima"
    }

    # Executa o método
    result = fallback_strategy.map_address_info(input_data)

    # Verifica se o mapeamento foi feito corretamente
    assert result == expected_output

def test_normalize_city(fallback_strategy):
    """Teste para verificar a normalização do nome da cidade."""
    city_input = "São Paulo"
    expected_output = "SAO PAULO"

    # Executa o método
    result = fallback_strategy._normalize_city(city_input)

    # Verifica se a cidade foi normalizada corretamente
    assert result == expected_output
