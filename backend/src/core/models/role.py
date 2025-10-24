from enum import Enum


# WARN:ROLE  impl with postgreql enum alembic https://pypi.org/project/alembic-postgresql-enum/
# Example
class Role(int, Enum):
    USER = 0
    ADMIN = 1
