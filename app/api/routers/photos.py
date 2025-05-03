from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.security import allow_create_edit, allow_all
from app.crud.photos import (
    add_photo_to_exhibit,
    get_photos_for_exhibit,
    delete_photo
)
from app.schemas.photos import PhotoCreate, PhotoResponse
from app.database.database import get_db

router = APIRouter(prefix="/api/exhibits/{exhibit_id}/photos")


@router.post("/",
             response_model=PhotoResponse,
             tags=["3Д-экспонаты"],
             dependencies=[Depends(allow_create_edit)])
def create_photo(
        exhibit_id: int,
        photo: PhotoCreate,
        db: Session = Depends(get_db)
):
    """Добавляет фотографию к 3Д-экспонату по ID 3Д-экспоната"""
    return add_photo_to_exhibit(db, exhibit_id, photo)

@router.get("/",
            response_model=List[PhotoResponse],
            tags=["3Д-экспонаты"],
            dependencies=[Depends(allow_all)])
def read_photos(
        exhibit_id: int,
        db: Session = Depends(get_db)
):
    """Возвращает список фотографий конкретного 3Д-экспоната по ID"""
    return get_photos_for_exhibit(db, exhibit_id)

@router.delete("/{photo_id}",
               tags=["3Д-экспонаты"],
               dependencies=[Depends(allow_create_edit)])
def remove_photo(
        photo_id: int,
        exhibit_id: int,
        db: Session = Depends(get_db)
):
    """Удаляет фото по ID фото и ID 3Д-экспоната"""
    deleted = delete_photo(db, photo_id, exhibit_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    return {"message": "Фото удалено"}
