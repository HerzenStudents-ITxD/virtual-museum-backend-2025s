from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.exhibit_links import (
    add_connected_to_exhibit,
    get_linked_exhibits,
    delete_linked_exhibit
)
from app.database.models import OtherExhibit
from app.schemas.exhibit_links import ConnectedExhibitCreate, ConnectedExhibitResponse, LinkedExhibitInfo
from app.database.database import get_db

router = APIRouter(prefix="/api/exhibits/{exhibit_id}/links")

#добавить ссылку к статье
@router.post("/", response_model=ConnectedExhibitResponse)
def create_link(
    exhibit_id: int,
    link: ConnectedExhibitCreate,
    db: Session = Depends(get_db)
):
    """Создает связь между текущим экспонатом и указанным в теле запроса"""
    try:
        return add_connected_to_exhibit(db, exhibit_id, link)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# получить все ссылки статьи
@router.get("/", response_model=List[LinkedExhibitInfo])
def read_links(
        exhibit_id: int,
        db: Session = Depends(get_db)
):
    links = get_linked_exhibits(db, exhibit_id)
    if not links:
        return []

    return [
        LinkedExhibitInfo(
            id=link.linked.id,
            title=link.linked.title,
            region=link.linked.region,
            main_photo=link.linked.main_photo
        )
        for link in links
        if link.linked
    ]

# удалить ссылку
@router.delete("/by-exhibit/{linked_exhibit_id}")
def remove_link_by_exhibit(
        exhibit_id: int,
        linked_exhibit_id: int,
        db: Session = Depends(get_db)
):
    link = db.query(OtherExhibit).filter(
        OtherExhibit.id_exhibit == exhibit_id,
        OtherExhibit.linked_exhibit_id == linked_exhibit_id
    ).first()

    if not link:
        raise HTTPException(status_code=404, detail="Связь не найдена")

    db.delete(link)
    db.commit()
    return {"message": "Связь удалена"}