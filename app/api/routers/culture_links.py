from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.culture_links import (
    add_connected_to_article,
    get_linked_articles,
    delete_linked_article
)
from app.database.models import OtherArticleCulture
from app.schemas.culture_links import ConnectedArticleCreate, ConnectedArticleResponse, LinkedArticleInfo
from app.database.database import get_db

router = APIRouter(prefix="/api/cultures/{culture_id}/links")


# добавить связь
@router.post("/", response_model=ConnectedArticleResponse)
def create_link(
        culture_id: int,
        link: ConnectedArticleCreate,
        db: Session = Depends(get_db)
):
    try:
        return add_connected_to_article(db, culture_id, link)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# получить все связи
@router.get("/", response_model=List[LinkedArticleInfo])
def read_links(
        culture_id: int,
        db: Session = Depends(get_db)
):
    links = get_linked_articles(db, culture_id)
    return [
        LinkedArticleInfo(
            id=link.linked.id,
            title=link.linked.title,
            region=link.linked.region,
            main_photo=link.linked.main_photo
        )
        for link in links
        if link.linked
    ]

# удалить по ID связанного экспоната
@router.delete("/by-linked/{linked_culture_id}")
def remove_link_by_linked_culture(
        culture_id: int,
        linked_culture_id: int,
        db: Session = Depends(get_db)
):
    """Удаляет связь по ID связанного экспоната"""
    try:
        # Находим связь по параметрам
        link = db.query(OtherArticleCulture).filter(
            OtherArticleCulture.id_culture == culture_id,
            OtherArticleCulture.linked_article == linked_culture_id
        ).first()

        if not link:
            raise HTTPException(status_code=404, detail="Связь не найдена")

        # Используем CRUD метод для удаления
        deleted = delete_linked_article(db, link.id, culture_id)
        return {
            "message": "Связь удалена",
            "deleted_link_id": deleted.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))