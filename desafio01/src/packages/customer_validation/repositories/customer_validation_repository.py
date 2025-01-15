from typing import List, Type

from src.database.models.customer_validation import ValidationRequestLogORM
from src.packages.customer_validation.repositories.customer_validation_repository_interface import (
    CustomerValidationRepositoryInterface,
)


class CustomerValidationRepository(CustomerValidationRepositoryInterface):
    def __init__(self, session_factory):
        # session_factory agora é uma função que retorna uma sessão.
        self._session_factory = session_factory

    async def save(self, entity: ValidationRequestLogORM) -> None:
        """Salva uma entidade no banco de dados."""
        async with self._session_factory() as session:  # Usamos o gerenciador de contexto
            session.add(entity)
            await session.commit()

    async def get_all(self) -> List[Type[ValidationRequestLogORM]]:
        """Retorna todas as entidades no banco de dados."""
        async with self._session_factory() as session:
            result = await session.execute(session.query(ValidationRequestLogORM))
            return result.scalars().all()
