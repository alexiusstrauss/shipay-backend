import pytest
from unittest.mock import MagicMock
from src.packages.customer_validation.repositories.validation_request_repository import ValidationRequestRepository
from src.database.models.customer_validation import ValidationRequestLogORM


def test_save_request():
    # Mock da sessão
    mock_session = MagicMock()

    # Instancia o repositório com o mock
    repository = ValidationRequestRepository(session=mock_session)

    # Dados de entrada
    cnpj = "12345678000195"
    cep = "12345678"
    result = True
    message = "Validation successful"

    # Chama o método save_request
    repository.save_request(cnpj, cep, result, message)

    # Verifica se add e commit foram chamados com os valores corretos
    mock_session.add.assert_called_once()
    added_log = mock_session.add.call_args[0][0]  # Obtém o objeto adicionado
    assert isinstance(added_log, ValidationRequestLogORM)
    assert added_log.cnpj == cnpj
    assert added_log.cep == cep
    assert added_log.result == result
    assert added_log.message == message

    mock_session.commit.assert_called_once()


def test_get_all_requests():
    # Mock da sessão e do retorno da consulta
    mock_session = MagicMock()
    mock_query = mock_session.query.return_value
    mock_query.all.return_value = [
        ValidationRequestLogORM(cnpj="12345678000195", cep="12345678", result=True, message="Validation successful"),
        ValidationRequestLogORM(cnpj="98765432000123", cep="87654321", result=False, message="Address mismatch"),
    ]

    # Instancia o repositório com o mock
    repository = ValidationRequestRepository(session=mock_session)

    # Chama o método get_all_requests
    result = repository.get_all_requests()

    # Verifica se a consulta foi feita na tabela correta
    mock_session.query.assert_called_once_with(ValidationRequestLogORM)

    # Verifica o resultado retornado
    assert len(result) == 2
    assert result[0].cnpj == "12345678000195"
    assert result[0].message == "Validation successful"
    assert result[1].cnpj == "98765432000123"
    assert result[1].message == "Address mismatch"
