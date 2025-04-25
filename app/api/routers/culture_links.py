from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.culture_links import (
    add_connected_to_article,
    get_linked_articles,
    delete_linked_article
)
from app.schemas.culture_links import ConnectedArticleCreate, ConnectedArticleResponse
from app.database.database import get_db

router = APIRouter(prefix="/api/culture/{culture_id}/links")

#Добавить ссылку к экспонату
@router.post("/", response_model=ConnectedArticleResponse)
def create_link(
        link: ConnectedArticleCreate,
        db: Session = Depends(get_db)
):
    return add_connected_to_article(db, link)


# Получить все ссылки экспоната
@router.get("/", response_model=List[ConnectedArticleResponse])
def read_links(
        culture_id: int,
        db: Session = Depends(get_db)
):
    return get_linked_articles(db, culture_id)

# Удалить ссылку
@router.delete("/{link_id}")
def remove_link(
        connected_id: int,
        culture_id: int,
        db: Session = Depends(get_db)
):
    deleted = delete_linked_article(db, connected_id, culture_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
    return {"message": "Ссылка удалена"}
