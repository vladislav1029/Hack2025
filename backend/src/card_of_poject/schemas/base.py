from pydantic import BaseModel
from uuid import UUID as PyUUID
from typing import Optional
from datetime import datetime


class ReferenceBase(BaseModel):
    name: str


class ReferenceCreate(ReferenceBase):
    pass


class ReferenceResponse(ReferenceBase):
    oid: PyUUID

    class Config:
        orm_mode = True


# INFO: для спрвочников и общих данных
