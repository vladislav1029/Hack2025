from sqlalchemy.orm import DeclarativeBase, declared_attr

import re
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__
        # Преобразуем CamelCase → snake_case
        snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        # Если уже заканчивается на 's' — не добавляем
        if snake_case.endswith("s"):
            return snake_case
        return snake_case + "s"