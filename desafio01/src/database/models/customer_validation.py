from sqlalchemy import Boolean, Column, Integer, String

try:
    from database.models.base_model import ORMBaseModel
except ModuleNotFoundError:
    from .base_model import ORMBaseModel


class ValidationRequestLogORM(ORMBaseModel):
    __tablename__ = "validation_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    result = Column(Boolean, nullable=False)
    message = Column(String, nullable=False)

    def __str__(self):
        return f"Validation: (cmpj={self.cnpj}, result={'True' if self.result else 'False'}, message={self.message})"
