from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.rest import init_middlewares, init_routes
from src.system.config import config


def create_app() -> FastAPI:
    """
    Função para criar e configurar a aplicação FastAPI.
    """
    app = FastAPI(title=config.PROJECT_NAME, version=config.APP_VERSION)  # NOQA

    # Inicializa middlewares
    init_middlewares(app)

    # Adiciona paginação global
    add_pagination(app)

    return app


# Instancia a aplicação
app = create_app()


@app.on_event("startup")
async def startup_event():
    """Inicializa rotas no evento de startup."""
    await init_routes(app)
