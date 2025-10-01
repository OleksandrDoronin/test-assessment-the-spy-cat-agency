from src.errors.base import NotFoundError


class MissionNotFoundError(NotFoundError): ...

class AssignedMissionCannotBeDeletedError(Exception): ...

class CannotUpdateCompletedMissionError(Exception):
    def __init__(self, msg: str = None):
        super().__init__(msg or 'Cannot update completed mission')

class CatAlreadyHasActiveMissionError(Exception):
    def __init__(self, msg: str = None):
        super().__init__(msg or 'Cat already has active mission')
