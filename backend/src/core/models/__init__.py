# INFO: Агрегатор для импорта.

__all__ = ["BaseTimeMixin", "BaseUUIDMixin", "BaseIDMixin"]
from .common import BaseTimeMixin
from .id import BaseIDMixin, BaseUUIDMixin
from .role import Role
