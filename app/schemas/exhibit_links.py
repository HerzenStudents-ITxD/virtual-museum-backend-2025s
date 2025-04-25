from typing import Optional
from pydantic import BaseModel

class ConnectedExhibitCreate(BaseModel):
    linked_exhibit_id: int

class ConnectedExhibitResponse(BaseModel):
    id: int
    id_exhibit: int
    linked_exhibit_id: int

    class Config:
        from_attributes = True

class LinkedExhibitInfo(BaseModel):
    id: int
    title: str
    region: Optional[str]
    main_photo: Optional[str]

    class Config:
        from_attributes = True