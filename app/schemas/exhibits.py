from pydantic import BaseModel, Field
from typing import Optional, List

class ExhibitCreate(BaseModel):
    title: str = Field(..., min_length=1)
    region: Optional[str] = None
    district: Optional[str] = None
    place: Optional[str] = None
    ethnos: Optional[str] = None
    desc: Optional[str] = None
    main_photo: Optional[str] = None

class ExhibitResponse(ExhibitCreate):
    id: int
    photos: List['PhotoResponse'] = []

    class Config:
        from_attributes = True

class PhotoResponse(BaseModel):
    id: int
    photo: str