from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


from uuid import UUID as PyUUID, uuid4


class BaseUUIDMixin:
    oid: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )


class BaseIDMixin:
    oid: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
