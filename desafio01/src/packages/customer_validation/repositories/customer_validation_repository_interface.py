from abc import ABC, abstractmethod
from typing import List

from src.database.models.customer_validation import ValidationRequestLogORM


class CustomerValidationRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, entity: ValidationRequestLogORM) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[ValidationRequestLogORM]:
        pass
