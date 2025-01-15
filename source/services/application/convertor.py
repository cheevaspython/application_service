from source.api.dependency.application.output_data import (
    ApplicationResponseData,
)
from source.db.models.application import Application


def convert_application_to_dataclass(
    application: Application,
) -> ApplicationResponseData:
    return ApplicationResponseData(
        id=application.id,
        user_name=application.user_name,
        description=application.description,
        created_date=application.created_date,
    )
