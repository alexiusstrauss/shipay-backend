import pytest
from unittest.mock import patch, MagicMock
from src.packages.customer_validation.factories.service_factory import (
    create_customer_validation_repository,
    create_cep_service,
    create_customer_validation_service,
    create_customer_validation_controller,
)
from src.packages.customer_validation.repositories.customer_validation_repository import CustomerValidationRepository
from src.packages.customer_validation.services.cep_service import CEPService
from src.packages.customer_validation.services.validation_service import ValidationService
from src.packages.customer_validation.controllers.customer_validation_controller import CustomerValidationController


def test_create_customer_validation_repository():
    with patch("src.database.get_db") as mock_get_db:
        mock_get_db.return_value = MagicMock()

        repository = create_customer_validation_repository()

        assert isinstance(repository, CustomerValidationRepository)
        assert callable(repository._session_factory)  # Corrigido para verificar '_session_factory'


def test_create_customer_validation_service():
    with patch("src.packages.customer_validation.factories.service_factory.create_customer_validation_repository") as mock_repo_factory, \
         patch("src.packages.customer_validation.factories.service_factory.create_cep_service") as mock_cep_service_factory, \
         patch("src.packages.customer_validation.factories.service_factory.CNPJServiceAdapter") as mock_cnpj_service_adapter:

        mock_repo = MagicMock()
        mock_cep_service = MagicMock()
        mock_cnpj_service = MagicMock()

        mock_repo_factory.return_value = mock_repo
        mock_cep_service_factory.return_value = mock_cep_service
        mock_cnpj_service_adapter.return_value = mock_cnpj_service

        validation_service = create_customer_validation_service()

        assert isinstance(validation_service, ValidationService)
        assert validation_service.repository == mock_repo
        assert validation_service.cep_service == mock_cep_service
        assert validation_service.cnpj_service == mock_cnpj_service


def test_create_customer_validation_controller():
    with patch("src.packages.customer_validation.factories.service_factory.create_customer_validation_service") as mock_service_factory:
        mock_service = MagicMock()
        mock_service_factory.return_value = mock_service

        controller = create_customer_validation_controller()

        assert isinstance(controller, CustomerValidationController)
        assert controller.service == mock_service
