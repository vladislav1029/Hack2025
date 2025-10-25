from pydantic import BaseModel
from uuid import UUID as PyUUID



class ReferenceBase(BaseModel):
    name: str


class ReferenceCreate(ReferenceBase):
    pass


class ReferenceResponse(ReferenceBase):
    oid: PyUUID

    class Config:
        from_attributes = True


# INFO: для спрвочников и общих данных
