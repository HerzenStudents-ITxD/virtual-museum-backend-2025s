from app.schemas.exhibits import ExhibitCreate, ExhibitResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from app.crud.exhibits import (
    get_exhibits,
    get_exhibit,
    create_exhibit
)
from app.database.database import get_db
from app.core.security import allow_create_edit, allow_all
from app.database.models import Exhibit

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

    exhibits = db.query(Exhibit)\
        .options(joinedload(Exhibit.photos))\
        .offset(skip).limit(count)

    if region:
        exhibits = exhibits.filter(Exhibit.region == region)
    if district:
        exhibits = exhibits.filter(Exhibit.district == district)
    if place:
        exhibits = exhibits.filter(Exhibit.place == place)
    if ethnos:
        exhibits = exhibits.filter(Exhibit.ethnos == ethnos)

    return exhibits.all()


@router.get("/{exhibit_id}",
            response_model=ExhibitResponse,
            tags=["3Д-экспонаты"],
            dependencies=[Depends(allow_all)])
def read_exhibit(exhibit_id: int,
                 db: Session = Depends(get_db)):
    """Возвращает конкретный 3Д-экспонат по ID"""
    db_exhibit = db.query(Exhibit)\
        .options(joinedload(Exhibit.photos))\
        .filter(Exhibit.id == exhibit_id)\
        .first()

    if not db_exhibit:
        raise HTTPException(status_code=404, detail="Экспонат не найден")

    return db_exhibit
