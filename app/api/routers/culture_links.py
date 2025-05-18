from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.security import allow_create_edit
from app.crud.culture_links import (
    add_connected_to_article,
    get_linked_articles,
    delete_linked_article
)
from app.database.models import OtherArticleCulture
from app.schemas.culture_links import ConnectedArticleCreate, ConnectedArticleResponse, LinkedArticleInfo
from app.database.database import get_db

router = APIRouter(prefix="/api/cultures/{culture_id}/links")


@router.post("/",
             response_model=ConnectedArticleResponse,
             tags=["Статьи из раздела Культура"],
             dependencies=[Depends(allow_create_edit)])
def create_link(
        culture_id: int,
        link: ConnectedArticleCreate,
        db: Session = Depends(get_db)
):
    """Создает связь между текущей статьёй и указанной в теле запроса"""
    try:
        return add_connected_to_article(db, culture_id, link)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/",
            response_model=List[LinkedArticleInfo],
            tags=["Статьи из раздела Культура"])
def read_links(
        culture_id: int,
        db: Session = Depends(get_db)
):
    """Возвращает список связей статьи по ID статьи"""
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

@router.delete("/by-linked/{linked_culture_id}",
               tags=["Статьи из раздела Культура"],
               dependencies=[Depends(allow_create_edit)])
def remove_link_by_linked_culture(
        culture_id: int,
        linked_culture_id: int,
        db: Session = Depends(get_db)
):
    """Удаляет связь по ID текущей и связанной статьи"""
    try:
        link = db.query(OtherArticleCulture).filter(
            OtherArticleCulture.id_culture == culture_id,
            OtherArticleCulture.linked_article == linked_culture_id
        ).first()

        if not link:
            raise HTTPException(status_code=404, detail="Связь не найдена")

        deleted = delete_linked_article(db, link.id, culture_id)
        return {
            "message": "Связь удалена",
            "deleted_link_id": deleted.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))