from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.exhibit_links import (
    add_connected_to_exhibit,
    get_linked_exhibits,
    delete_linked_exhibit
)
from app.schemas.exhibit_links import ConnectedExhibitCreate, ConnectedExhibitResponse
from app.database.database import get_db

router = APIRouter(prefix="/api/exhibits/{exhibit_id}/links")

#Добавить ссылку к статье
@router.post("/", response_model=ConnectedExhibitResponse)
def create_link(
        link: ConnectedExhibitCreate,
        db: Session = Depends(get_db)
):
    return add_connected_to_exhibit(db, link)


# Получить все ссылки статьи
@router.get("/", response_model=List[ConnectedExhibitResponse])
def read_links(
        exhibit_id: int,
        db: Session = Depends(get_db)
):
    return get_linked_exhibits(db, exhibit_id)

# Удалить ссылку
@router.delete("/{link_id}")
def remove_link(
        connected_id: int,
        exhibit_id: int,
        db: Session = Depends(get_db)
):
    deleted = delete_linked_exhibit(db, connected_id, exhibit_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
    return {"message": "Ссылка удалена"}
