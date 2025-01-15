from dataclasses import dataclass

from source.common.error import ApplicationError


@dataclass(eq=False)
class CannotSaveApplicationError(ApplicationError):

    @property
    def message(self):
        return "Cannot save application"


@dataclass(eq=False)
class CreateDateSerializeError(ApplicationError):

    @property
    def message(self):
        return "Create date type not serializable"
