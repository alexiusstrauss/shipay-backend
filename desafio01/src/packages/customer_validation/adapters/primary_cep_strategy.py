import httpx
import unicodedata
from typing import Dict
from src.packages.customer_validation.ports.cep_strategy_interface import CEPStrategyInterface


class PrimaryCEPStrategy(CEPStrategyInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def map_address_info(self, address_info: Dict) -> Dict:
        return {
            "state": address_info["state"],
            "city": self._normalize_city(address_info["city"]),
            "street": address_info["street"],
        }

    async def get_address_info(self, cep: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/{cep}")
            response.raise_for_status()
            return response.json()

    def _normalize_city(self, city: str) -> str:
        """
        Normaliza o nome da cidade removendo acentos e convertendo para maiúsculas.
        """
        # Remove acentos
        normalized = unicodedata.normalize('NFD', city)
        normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
        # Converte para maiúsculas
        return normalized.upper()