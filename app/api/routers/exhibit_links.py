from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.security import allow_create_edit
from app.crud.exhibit_links import (
    add_connected_to_exhibit,
    get_linked_exhibits,
    delete_linked_exhibit
)
from app.database.models import OtherExhibit
from app.schemas.exhibit_links import ConnectedExhibitCreate, ConnectedExhibitResponse, LinkedExhibitInfo
from app.database.database import get_db

router = APIRouter(prefix="/api/exhibits/{exhibit_id}/links")


@router.post("/",
             response_model=ConnectedExhibitResponse,
             tags=["3Д-экспонаты"],
             dependencies=[Depends(allow_create_edit)])
def create_link(
    exhibit_id: int,
    link: ConnectedExhibitCreate,
    db: Session = Depends(get_db)
):
    """Создает связь между текущим 3Д-экспонатом и указанным в теле запроса"""
    try:
        return add_connected_to_exhibit(db, exhibit_id, link)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/",
            response_model=List[LinkedExhibitInfo],
            tags=["3Д-экспонаты"])
def read_links(
        exhibit_id: int,
        db: Session = Depends(get_db)
):
    """Возвращает список связей 3Д-экспоната по ID 3Д-экспоната"""
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

@router.delete("/by-exhibit/{linked_exhibit_id}",
               tags=["3Д-экспонаты"],
               dependencies=[Depends(allow_create_edit)])
def remove_link_by_exhibit(
        exhibit_id: int,
        linked_exhibit_id: int,
        db: Session = Depends(get_db)
):
    """Удаляет связь по ID текущего и связанного 3Д-экспоната"""
    try:
        link = db.query(OtherExhibit).filter(
            OtherExhibit.id_exhibit == exhibit_id,
            OtherExhibit.linked_exhibit_id == linked_exhibit_id
        ).first()

        if not link:
            raise HTTPException(status_code=404, detail="Связь не найдена")

        deleted = delete_linked_exhibit(db, link.id, exhibit_id)
        return {
            "message": "Связь удалена",
            "deleted_link_id": deleted.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
