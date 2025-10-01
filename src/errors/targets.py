from src.errors.base import NotFoundError


class TargetNotFoundError(NotFoundError): ...

class CannotUpdateCompletedTargetError(Exception):
    def __init__(self, msg: str = None):
        super().__init__(msg or 'Cannot update completed target')
