from dataclasses import dataclass

from source.common.error import ApplicationError


@dataclass(eq=False)
class CannotSaveApplicationError(ApplicationError):

    @property
    def message(self):
        return "Cannot save application"
