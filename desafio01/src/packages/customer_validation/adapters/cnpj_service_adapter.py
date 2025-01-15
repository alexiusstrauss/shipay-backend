import httpx

from src.packages.customer_validation.ports.cnpj_service_interface import (
    CNPJServiceInterface,
)


class CNPJServiceAdapter(CNPJServiceInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_company_info(self, cnpj: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/{cnpj}")
            response.raise_for_status()

            data = response.json()
            # Ajusta o logradouro para incluir descricao_tipo_de_logradouro
            if "logradouro" in data and "descricao_tipo_de_logradouro" in data:
                data["logradouro"] = f"{data['descricao_tipo_de_logradouro']} {data['logradouro']}"

            return data