from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database.models import OtherExhibit, Exhibit
from app.schemas.exhibit_links import ConnectedExhibitCreate

"""
linked_exhibit_id - id присоёдиненного экспоната
id_exhibit - id экспоната, к которому присоединяют
exhibit_id - то же что id_exhibit, но передаётся при запросе и вводится пользователем
"""


def add_connected_to_exhibit(db: Session, exhibit_id: int, connected: ConnectedExhibitCreate):
    # проверяем существование обоих экспонатов
    if not db.get(Exhibit, exhibit_id):
        raise HTTPException(status_code=404, detail="Основной экспонат не найден")
    if not db.get(Exhibit, connected.linked_exhibit_id):
        raise HTTPException(status_code=404, detail="Связанный экспонат не найден")

    # проверяем, что связь не дублируется
    existing = db.query(OtherExhibit).filter(
        OtherExhibit.id_exhibit == exhibit_id,
        OtherExhibit.linked_exhibit_id == connected.linked_exhibit_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Связь уже существует")

    # создаем новую связь
    db_connected = OtherExhibit(
        id_exhibit=exhibit_id,
        linked_exhibit_id=connected.linked_exhibit_id
    )

    db.add(db_connected)
    db.commit()
    db.refresh(db_connected)
    return db_connected

def get_linked_exhibits(db: Session, exhibit_id: int):
    return db.query(OtherExhibit)\
        .options(
            joinedload(OtherExhibit.linked)
        )\
        .filter(OtherExhibit.id_exhibit == exhibit_id)\
        .all()


def delete_linked_exhibit(db: Session, link_id: int, exhibit_id: int):
    # сначала проверяем существование связи без привязки к exhibit_id
    link = db.query(OtherExhibit).filter(OtherExhibit.id == link_id).first()

    if not link:
        raise ValueError(f"Связь с ID {link_id} не найдена")

    # затем проверяем принадлежность к экспонату
    if link.id_exhibit != exhibit_id:
        raise ValueError(
            f"Связь {link_id} принадлежит экспонату {link.id_exhibit}, а не {exhibit_id}"
        )

    try:
        db.delete(link)
        db.commit()
        return link
    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка БД при удалении: {str(e)}")