from app.schemas.exhibits import ExhibitCreate, ExhibitResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.crud.exhibits import (
    get_exhibits,
    get_exhibit,
    create_exhibit
)
from app.database.database import get_db
from app.core.security import allow_create_edit, allow_all

router = APIRouter(prefix="/api/exhibits")

@router.post("/",
             response_model=ExhibitResponse,
             tags=["3Д-экспонаты"],
             dependencies=[Depends(allow_create_edit)])
def create_exhibit_endpoint(
    exhibit: ExhibitCreate,
    db: Session = Depends(get_db)
):
    """Создаёт новый 3Д-экспонат"""
    try:
        db_exhibit = create_exhibit(db, exhibit)
        return db_exhibit
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
            response_model=list[ExhibitResponse],
            tags=["3Д-экспонаты"],
            dependencies=[Depends(allow_all)])
def read_exhibits(
    page: int = Query(1, ge=1, description="Номер страницы (начиная с 1)"),
    count: int = Query(20, ge=1, le=20, description="Количество на странице (макс. 20)"),
    region: Optional[str] = Query(None, description="Фильтр по региону"),
    district: Optional[str] = Query(None, description="Фильтр по району"),
    place: Optional[str] = Query(None, description="Фильтр по населённому пункту"),
    ethnos: Optional[str] = Query(None, description="Фильтр по этносу"),
    db: Session = Depends(get_db)
):
    """Возвращает список 3Д-экспонатов (с фильтрацией и пагинацией)"""
    skip = (page - 1) * count
    return get_exhibits(
        db,
        skip=skip,
        limit=count,
        region=region,
        district=district,
        place=place,
        ethnos=ethnos
    )

@router.get("/{exhibit_id}",
            response_model=ExhibitResponse,
            tags=["3Д-экспонаты"],
            dependencies=[Depends(allow_all)])
def read_exhibit(exhibit_id: int,
                 db: Session = Depends(get_db)):
    """Возвращает конкретный 3Д-экспонат по ID"""
    db_exhibit = get_exhibit(db, exhibit_id)
    if not db_exhibit:
        raise HTTPException(status_code=404, detail="Экспонат не найден")
    return db_exhibit