from sqlalchemy.orm import Session
from app.database.models import Exhibit
from app.schemas.exhibits import ExhibitCreate

def get_exhibit(db: Session, exhibit_id: int):
    return db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()

def get_exhibits(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        region: str | None = None,
        district: str | None = None,
        place: str | None = None,
        ethnos: str | None = None
):
    query = db.query(Exhibit)

    # фильтры
    if region:
        query = query.filter(Exhibit.region == region)
    if district:
        query = query.filter(Exhibit.district == district)
    if place:
        query = query.filter(Exhibit.place == place)
    if ethnos:
        query = query.filter(Exhibit.ethnos == ethnos)


    return query.offset(skip).limit(limit).all()

def create_exhibit(db: Session, exhibit_data: ExhibitCreate):
    try:
        db_exhibit = Exhibit(
            title=exhibit_data.title,
            region=exhibit_data.region,
            district=exhibit_data.district,
            place=exhibit_data.place,
            ethnos=exhibit_data.ethnos,
            desc=exhibit_data.desc,
            main_photo=exhibit_data.main_photo
        )

        db.add(db_exhibit)
        db.commit()
        db.refresh(db_exhibit)
        return db_exhibit

    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка базы данных: {str(e)}")