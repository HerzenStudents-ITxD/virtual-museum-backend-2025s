from sqlalchemy.orm import Session
from app.database.models import Exhibit, PhotoExhibit, OtherExhibit
from app.schemas.exhibits import ExhibitCreate, PhotoCreate, LinkedExhibitCreate

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
        # Создание основного экспоната
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
        db.flush()  # получаем id до commit

        # Добавление фотографий
        if exhibit_data.photos:
            for photo in exhibit_data.photos:
                db_photo = PhotoExhibit(
                    photo=photo.photo,
                    id_exhibit=db_exhibit.id
                )
                db.add(db_photo)

        # Добавление связанных экспонатов
        if exhibit_data.linked_exhibits:
            for link in exhibit_data.linked_exhibits:
                db_link = OtherExhibit(
                    id_exhibit=db_exhibit.id,
                    linked_exhibit_id=link.linked_exhibit_id
                )
                db.add(db_link)

        db.commit()
        db.refresh(db_exhibit)
        return db_exhibit

    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка базы данных: {str(e)}")
