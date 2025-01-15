import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class ORMBaseModel:
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __name__: str

    def update(self, **fields):
        for key, value in fields.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return cls.__name__.lower()
