from typing import Optional
from pydantic import BaseModel

class ConnectedExhibitBase(BaseModel):
    linked_exhibit_id: int
    id_exhibit: int

class ConnectedExhibitCreate(ConnectedExhibitBase):
    pass

class ConnectedExhibitResponse(ConnectedExhibitBase):
    id: int

    class Config:
        from_attributes = True
#!!!!!подумать над этим!!!!
class LinkedExhibitInfo(BaseModel):
    id: int
    title: str
    main_photo: Optional[str]