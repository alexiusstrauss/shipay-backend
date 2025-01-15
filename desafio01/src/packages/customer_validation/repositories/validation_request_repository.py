from sqlalchemy.orm import Session

from src.database.models.customer_validation import ValidationRequestLogORM


class ValidationRequestRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_request(self, cnpj: str, cep: str, result: bool, message: str):
        log = ValidationRequestLogORM(cnpj=cnpj, cep=cep, result=result, message=message)
        self.session.add(log)
        self.session.commit()

    def get_all_requests(self):
        return self.session.query(ValidationRequestLogORM).all()
