from fastapi import BackgroundTasks

from src.packages.customer_validation.ports.cep_strategy_interface import CEPStrategyInterface
from src.database.models.customer_validation import ValidationRequestLogORM
from src.packages.customer_validation.ports.cnpj_service_interface import (
    CNPJServiceInterface,
)
from src.packages.customer_validation.repositories.customer_validation_repository import (
    CustomerValidationRepository,
)
from src.packages.customer_validation.schemas.validation_schemas import (
    ValidationRequest,
    ValidationResponse,
)
from src.packages.customer_validation.services.cep_service import CEPService


class ValidationService:
    def __init__(
        self,
        cnpj_service: CNPJServiceInterface,
        cep_service: CEPService,
        repository: CustomerValidationRepository,
    ):
        self.cnpj_service = cnpj_service
        self.cep_service = cep_service
        self.repository = repository

    async def validate(self, request: ValidationRequest, strategies: list) -> ValidationResponse:
        for strategy in strategies:
            try:
                external_info = await self._get_external_data(request, strategy)

                is_valid = (
                    external_info["cnpj_info"]["uf"] == external_info["address_info"]["state"]
                    and external_info["cnpj_info"]["municipio"].lower() == external_info["address_info"][
                        "city"
                    ].lower()
                    and external_info["cnpj_info"]["logradouro"].lower() == external_info["address_info"][
                        "street"
                    ].lower()
                )

                msg_result = "Validation successful" if is_valid else "Address mismatch"
                await self.save_validation_request(request, valid=is_valid, message=msg_result)
                if is_valid:
                    return ValidationResponse(valid=is_valid, message=msg_result)
            except Exception as e:
                print(f"Erro com a estratégia {strategy.__class__.__name__}: {e}")

        print("Nenhuma estratégia validou com sucesso.")
        return ValidationResponse(valid=False, message="Validation failed after all retries.")


    async def _get_external_data(self, request: ValidationRequest, strategy: CEPStrategyInterface) -> dict:
        try:
            cnpj_info = await self.cnpj_service.get_company_info(request.cnpj)
            address_info = await strategy.get_address_info(request.cep)
            mapped_address = strategy.map_address_info(address_info)
            return {"cnpj_info": cnpj_info, "address_info": mapped_address}
        except Exception as e:
            print(f"Erro ao obter dados externos com a estratégia {strategy.__class__.__name__}: {e}")
            raise e

    async def save_validation_request(self, request: ValidationRequest, valid: bool, message: str):
        try:
            await self.repository.save(
                ValidationRequestLogORM(
                    **request.model_dump(),
                    result=valid,
                    message=message
                )
            )
        except Exception as e:
            print(f"Erro ao salvar no banco de dados: {e}")
            raise e

    async def retry_validation_task(self, request: ValidationRequest):
        try:
            print("Retentativa de validação iniciada...")
            return await self.validate(request, self.cep_service.strategies)
        except Exception as e:
            print(f"Retentativa falhou: {e}")
            return ValidationResponse(valid=False, message="Validation failed after retry.")

    def schedule_retry(self, request: ValidationRequest, background_tasks: BackgroundTasks):
        background_tasks.add_task(self.retry_validation_task, request)
