from abc import ABC, abstractmethod


class CNPJServiceInterface(ABC):
    @abstractmethod
    async def get_company_info(self, cnpj: str) -> dict:
        ...
