from dataclasses import dataclass

from source.common.error import ApplicationError


@dataclass(eq=False)
class CustomDoesNotExist(ApplicationError):

    class_name: str
    model_id: int | None = None

    @property
    def message(self):
        # add logger TODO
        return f"{self.class_name} does not exist with id: {self.model_id}"
