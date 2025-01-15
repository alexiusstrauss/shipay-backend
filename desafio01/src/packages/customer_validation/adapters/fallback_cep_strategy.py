import httpx
import unicodedata
from typing import Dict
from src.packages.customer_validation.ports.cep_strategy_interface import CEPStrategyInterface


class FallbackCEPStrategy(CEPStrategyInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def map_address_info(self, address_info: Dict) -> Dict:
        return {
            "state": address_info["uf"],
            "city": self._normalize_city(address_info["localidade"]),
            "street": address_info["logradouro"],
        }

    async def get_address_info(self, cep: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/{cep}/json/")
            response.raise_for_status()
            return response.json()

    def _normalize_city(self, city: str) -> str:
        normalized = unicodedata.normalize('NFD', city)
        normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
        return normalized.upper()