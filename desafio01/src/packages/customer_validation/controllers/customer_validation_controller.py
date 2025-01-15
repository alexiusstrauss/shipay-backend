from fastapi import APIRouter, BackgroundTasks, Body, status
from fastapi.responses import JSONResponse
from src.system.config import config
from src.packages.customer_validation.schemas.validation_schemas import ValidationRequest, ValidationResponse
from src.packages.customer_validation.ports.validation_service_interface import ValidationServiceInterface
from src.packages.customer_validation.adapters.primary_cep_strategy import PrimaryCEPStrategy
from src.packages.customer_validation.adapters.fallback_cep_strategy import FallbackCEPStrategy


class CustomerValidationController:
    def __init__(self, validation_service: ValidationServiceInterface):
        self.service = validation_service
        self.router = APIRouter()

        self.router.add_api_route(
            "/",
            self.validate_customer,
            methods=["POST"],
            response_model=ValidationResponse,
            status_code=status.HTTP_200_OK,
            summary="Validação de Cliente",
            description="Valida os dados do cliente usando CNPJ e CEP.",
        )

    async def validate_customer(
        self, request: ValidationRequest = Body(...), background_tasks: BackgroundTasks = None
    ) -> JSONResponse:
        strategies = [FallbackCEPStrategy(config.FALLBACK_CEP_API), PrimaryCEPStrategy(config.PRIMARY_CEP_API)]
        response = await self.service.validate(request, strategies)

        if not response.valid:
            if background_tasks:
                self.service.schedule_retry(request, background_tasks)
            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_200_OK)
