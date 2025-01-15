from typing import Any, Union


class CommonException(Exception):
    """Base exception class for all exceptions in this project."""

    code: int
    message: str
    detail: Union[Any, None]

    def __init__(self, code: int = 400, message: str = 'Bad Request', detail: Union[Any, None] = None):
        self.code = code
        self.message = message
        self.detail = detail

    def __str__(self):
        return f'''
            code: {self.code}
            message: {self.message}
            detail: {self.detail}
            traceback: {self.__traceback__}
            '''

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'detail': self.detail,
        }


class BadRequestError(CommonException):
    def __init__(self, message: str = None, detail: str = None):
        super().__init__(
            code=400,
            message=message or "Bad Request",
            detail=detail or "Os dados fornecidos estão incorretos ou incompletos.",
        )


class UnauthorizedError(CommonException):
    def __init__(self, message: str = None, detail: str = None):
        super().__init__(
            code=401,
            message=message or "Unauthorized",
            detail=detail or "A autenticação é necessária ou falhou.",
        )


class ForbiddenError(CommonException):
    def __init__(self, message: str = None, detail: str = None):
        super().__init__(
            code=403,
            message=message or "Forbidden",
            detail=detail or "Você não tem permissão para acessar este recurso.",
        )


class NotFoundError(CommonException):
    def __init__(self, message: str = None, detail: str = None):
        super().__init__(
            code=404,
            message=message or "Not Found",
            detail=detail or "O recurso solicitado não foi encontrado.",
        )


class ConflictError(CommonException):
    def __init__(self, message: str = None, detail: str = None):
        super().__init__(
            code=409,
            message=message or "Conflict",
            detail=detail or "Há um conflito com o estado atual do recurso.",
        )


class InternalServerError(CommonException):
    def __init__(self, message: str = None, detail: str = None):
        super().__init__(
            code=500,
            message=message or "Internal Server Error",
            detail=detail or "Ocorreu um erro inesperado no servidor.",
        )


class ServiceUnavailableError(CommonException):
    def __init__(self, message: str = None, detail: str = None):
        super().__init__(
            code=503,
            message=message or "Service Unavailable",
            detail=detail or "O serviço está temporariamente indisponível.",
        )
