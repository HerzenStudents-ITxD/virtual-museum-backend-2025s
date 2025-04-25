from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database.models import OtherArticleCulture, Culture
from app.schemas.culture_links import ConnectedArticleCreate

"""
linked_article_id - id присоёдиненного экспоната
id_culture - id экспоната, к которому присоединяют
culture_id - то же что id_exhibit, но передаётся при запросе и вводится пользователем
"""


def add_connected_to_article(db: Session, culture_id: int, connected: ConnectedArticleCreate):
    # проверка существования объектов
    if not db.get(Culture, culture_id):
        raise HTTPException(status_code=404, detail="Основной экспонат не найден")
    if not db.get(Culture, connected.linked_article_id):
        raise HTTPException(status_code=404, detail="Связанный экспонат не найден")

    # проверка на дубликат
    existing = db.query(OtherArticleCulture).filter(
        OtherArticleCulture.id_culture == culture_id,
        OtherArticleCulture.linked_article == connected.linked_article_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Связь уже существует")

    # создание и сохранение связи
    db_connected = OtherArticleCulture(
        id_culture=culture_id,
        linked_article=connected.linked_article_id
    )
    db.add(db_connected)
    db.commit()
    db.refresh(db_connected)

    # возвращаем словарь вместо SQLAlchemy модели
    return {
        "id": db_connected.id,
        "id_culture": db_connected.id_culture,
        "linked_article_id": db_connected.linked_article
    }

def get_linked_articles(db: Session, culture_id: int):
    """Получить связанные экспонаты с полной информацией"""
    return db.query(OtherArticleCulture)\
        .options(
            joinedload(OtherArticleCulture.linked)
        )\
        .filter(OtherArticleCulture.id_culture == culture_id)\
        .all()

def delete_linked_article(db: Session, link_id: int, culture_id: int):
    """Удаляет связь с дополнительной проверкой"""
    # сначала проверяем существование связи без привязки к exhibit_id
    link = db.query(OtherArticleCulture).filter(OtherArticleCulture.id == link_id).first()

    if not link:
        raise ValueError(f"Связь с ID {link_id} не найдена")

    # затем проверяем принадлежность к экспонату
    if link.id_culture != culture_id:
        raise ValueError(
            f"Связь {link_id} принадлежит экспонату {link.id_culture}, а не {culture_id}"
        )

    try:
        db.delete(link)
        db.commit()
        return link
    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка БД при удалении: {str(e)}")