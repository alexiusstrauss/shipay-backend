import pytest
from unittest.mock import AsyncMock
from src.packages.customer_validation.services.cep_service import CEPService
from src.packages.customer_validation.adapters.primary_cep_strategy import PrimaryCEPStrategy
from src.packages.customer_validation.adapters.fallback_cep_strategy import FallbackCEPStrategy


@pytest.mark.asyncio
async def test_cep_service_all_failures():
    primary_strategy = AsyncMock()
    fallback_strategy = AsyncMock()

    # Configurar mock para falha em ambas as estratégias
    primary_strategy.get_address_info.side_effect = Exception("Primary falhou")
    fallback_strategy.get_address_info.side_effect = Exception("Fallback falhou")

    cep_service = CEPService([fallback_strategy, primary_strategy])

    with pytest.raises(Exception, match="Todas as estratégias falharam"):
        await cep_service.get_address_info("57045310")

    primary_strategy.get_address_info.assert_called_once_with("57045310")
    fallback_strategy.get_address_info.assert_called_once_with("57045310")