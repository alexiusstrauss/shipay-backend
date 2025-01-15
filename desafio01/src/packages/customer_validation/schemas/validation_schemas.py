import re

from pydantic import BaseModel, Field, field_validator


class ValidationRequest(BaseModel):
    cnpj: str = Field(..., description="CNPJ do cliente em formato válido.")
    cep: str = Field(..., description="CEP do cliente em formato válido.")

    @field_validator("cnpj")
    def validate_cnpj(cls, value: str) -> str:
        cnpj_cleaned = re.sub(r"\D", "", value)

        if not cnpj_cleaned.isdigit() or len(cnpj_cleaned) != 14:
            raise ValueError("CNPJ inválido. Deve conter 14 dígitos.")

        return cnpj_cleaned

    @field_validator("cep")
    def validate_cep(cls, value: str) -> str:
        cep_cleaned = re.sub(r"\D", "", value)

        if not cep_cleaned.isdigit() or len(cep_cleaned) != 8:
            raise ValueError("CEP inválido. Deve conter 8 dígitos.")

        return cep_cleaned


class ValidationResponse(BaseModel):
    valid: bool
    message: str
