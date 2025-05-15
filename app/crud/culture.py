from typing import Optional
from sqlalchemy.orm import Session
from app.database.models import Culture, CultureTypeEnum
from app.schemas.culture import CultureCreate

#получить конкретную статью
def get_culture_article(db: Session, culture_id: int):
    return db.query(Culture).filter(Culture.id == culture_id).first()

#добавить статью
def create_culture(db: Session, culture: CultureCreate):
    db_culture = Culture(**culture.model_dump())
    db.add(db_culture)
    db.commit()
    db.refresh(db_culture)
    return db_culture

#получить статьи с фильтром
def get_culture_articles(
        db: Session,
        type: Optional[CultureTypeEnum] = None,  # делаем параметр опциональным
        skip: int = 0,
        limit: int = 100
):

    query = db.query(Culture)

    # фильтрация по типу (если передан)
    if type is not None:
        query = query.filter(Culture.type == type)


    return query.offset(skip).limit(limit).all()