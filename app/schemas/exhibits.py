from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.exhibits import PhotoResponse  # для forward references

# --- Основные схемы для Exhibit ---

class ExhibitBase(BaseModel):
    title: str = Field(..., min_length=1)
    region: Optional[str] = None
    district: Optional[str] = None
    place: Optional[str] = None
    ethnos: Optional[str] = None
    desc: Optional[str] = None
    main_photo: Optional[str] = None

class PhotoCreate(BaseModel):
    photo: str

class LinkedExhibitCreate(BaseModel):
    linked_exhibit_id: int

# --- Создание экспоната ---

class ExhibitCreate(ExhibitBase):
    photos: Optional[List[PhotoCreate]] = []
    linked_exhibits: Optional[List[LinkedExhibitCreate]] = []

# --- Ответ на создание или запрос ---

class PhotoResponse(BaseModel):
    id: int
    photo: str
    id_exhibit: int

    class Config:
        from_attributes = True

class ExhibitResponse(ExhibitBase):
    id: int
    photos: List[PhotoResponse] = []

    class Config:
        from_attributes = True
