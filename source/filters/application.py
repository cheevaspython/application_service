from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ApplicationFilters:
    user_name: str | None = None
