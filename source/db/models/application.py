from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from source.db.models import Base
from source.db.models.mixins.create_update import CreateUpdateMixin
from source.db.models.mixins.id_int_pk import IdBigIntPkMixin


class Application(
    Base,
    IdBigIntPkMixin,
    CreateUpdateMixin,
):

    _back_populates = "applications"

    user_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        String(),
    )
