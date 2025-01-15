from abc import ABC, abstractmethod
from typing import Dict


class CEPStrategyInterface(ABC):
    @abstractmethod
    def map_address_info(self, address_info: Dict) -> Dict:
        """
        Mapeia os dados de endereço para os atributos comuns de validação.

        :param address_info: Informações de endereço retornadas pela API de CEP.
        :return: Um dicionário contendo os dados mapeados.
        """
        ...

    @abstractmethod
    async def get_address_info(self, cep: str) -> dict:
        ...
