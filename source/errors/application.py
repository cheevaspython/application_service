from dataclasses import dataclass

from source.common.error import ApplicationError
from source.services.logging import logger


@dataclass(eq=False)
class CannotSaveApplicationError(ApplicationError):

    @property
    def message(self):
        logger.warning("Cannot save application")
        return "Cannot save application"


@dataclass(eq=False)
class CreateDateSerializeError(ApplicationError):

    @property
    def message(self):
        logger.warning("Create date type not serializable")
        return "Create date type not serializable"
