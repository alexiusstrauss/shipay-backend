from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.packages.customer_validation.factories.service_factory import (
    create_customer_validation_controller,
)


def init_middlewares(app: FastAPI):
    """
    Inicializa middlewares na aplicação FastAPI.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def init_routes(app: FastAPI):
    """
    Configura as rotas da aplicação FastAPI.
    """
    # Cria o controlador de validação de cliente
    customer_validation_controller = create_customer_validation_controller()

    # Adiciona as rotas do controlador
    app.include_router(
        customer_validation_controller.router,
        prefix="/customer-validation",
        tags=["Customer Validation"],
    )
