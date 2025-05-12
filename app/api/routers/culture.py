from app.core.security import allow_create_edit, allow_all
from app.database.models import CultureTypeEnum
from app.schemas.culture import CultureCreate, CultureResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.crud.culture import (
    get_culture_article,
    get_culture_articles,
    create_culture
)
from app.database.database import get_db

router = APIRouter(prefix="/api/culture")

@router.post("/",
             response_model=CultureResponse,
             tags=["Статьи из раздела Культура"],
             dependencies=[Depends(allow_create_edit)])
def create_culture_endpoint(
    culture: CultureCreate,
    db: Session = Depends(get_db)
):
    """Создаёт новую статью Культуры"""
    try:
        db_culture = create_culture(db, culture)
        return db_culture
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
            response_model=List[CultureResponse],
            tags=["Статьи из раздела Культура"],
            dependencies=[Depends(allow_all)])
def read_culture_articles(
    type: Optional[CultureTypeEnum] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=500),
    db: Session = Depends(get_db)
):
    """Возвращает список статей (с фильтрацией и пагинацией)"""
    return get_culture_articles(
        db,
        type=type,
        skip=skip,
        limit=limit
    )

@router.get("/{culture_id}",
            response_model=CultureResponse,
            tags=["Статьи из раздела Культура"],
            dependencies=[Depends(allow_all)])
def read_culture_article(
        culture_id: int,
        db: Session = Depends(get_db)):
    """Возвращает конкретную статью по ID"""
    db_culture = get_culture_article(db, culture_id)
    if not db_culture:
        raise HTTPException(status_code=404, detail="Экспонат не найден")
    return db_culture