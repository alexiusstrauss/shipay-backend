from typing import List

from src.packages.customer_validation.ports.cep_strategy_interface import (
    CEPStrategyInterface,
)


class CEPService:
    def __init__(self, strategies: List[CEPStrategyInterface]):
        self.strategies = strategies

    async def get_address_info(self, cep: str, retries_per_strategy: int = 1) -> dict:
        last_exception = None

        for strategy in self.strategies:
            for attempt in range(retries_per_strategy):
                try:
                    print(f"Tentando com {strategy.__class__.__name__}, tentativa {attempt + 1}")
                    return await strategy.get_address_info(cep)
                except Exception as e:
                    last_exception = e
                    print(f"Falha na tentativa {attempt + 1} com {strategy.__class__.__name__}: {str(e)}")
                    break
        raise Exception(f"Todas as estratégias falharam. Último erro: {last_exception}")
