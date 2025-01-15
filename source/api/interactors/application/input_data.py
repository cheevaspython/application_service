from dataclasses import dataclass


@dataclass(frozen=True)
class CreateApplicationInputData:
    user_name: str
    description: str
