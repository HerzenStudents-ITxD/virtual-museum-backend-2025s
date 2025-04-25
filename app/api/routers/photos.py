from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.photos import (
    add_photo_to_exhibit,
    get_photos_for_exhibit,
    delete_photo
)
from app.schemas.photos import PhotoCreate, PhotoResponse
from app.database.database import get_db

router = APIRouter(prefix="/api/exhibits/{exhibit_id}/photos")


# Добавить фото
@router.post("/", response_model=PhotoResponse)
def create_photo(
        exhibit_id: int,
        photo: PhotoCreate,
        db: Session = Depends(get_db)
):
    return add_photo_to_exhibit(db, exhibit_id, photo)


# Получить все фото экспоната
@router.get("/", response_model=List[PhotoResponse])
def read_photos(
        exhibit_id: int,
        db: Session = Depends(get_db)
):
    return get_photos_for_exhibit(db, exhibit_id)


# Удалить фото
@router.delete("/{photo_id}")
def remove_photo(
        photo_id: int,
        exhibit_id: int,
        db: Session = Depends(get_db)
):
    deleted = delete_photo(db, photo_id, exhibit_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    return {"message": "Фото удалено"}
