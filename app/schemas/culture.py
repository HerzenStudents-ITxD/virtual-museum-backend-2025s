from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class CultureTypeEnum(str, Enum):
    DECORATIVE = "Декоративно-прикладное искусство"
    VERBAL = "Устное народное творчество"
    MUSIC = "Танцевально-музыкальная культура"

class CultureCreate(BaseModel):
    type: CultureTypeEnum = None
    title: str = Field(..., min_length=1)
    region: Optional[str] = None
    district: Optional[str] = None
    place: Optional[str] = None
    ethnos: Optional[str] = None
    desc: Optional[str] = None
    main_photo: Optional[str] = None
    author: Optional[str] = None
    model: Optional[str] = None
    creation_date: Optional[str] = None
    location: Optional[str] = None

class CultureResponse(CultureCreate):
    id: int

    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    id: int
    type: str