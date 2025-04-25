from sqlalchemy.orm import Session
from app.database.models import OtherArticleCulture
from app.schemas.culture_links import ConnectedArticleCreate

"""
linked_article_id - id присоёдиненного экспоната
id_culture - id экспоната, к которому присоединяют
culture_id - то же что id_exhibit, но передаётся при запросе и вводится пользователем
"""

def add_connected_to_article(db: Session, connected: ConnectedArticleCreate):
    db_connected = OtherArticleCulture(**connected.model_dump())
    db.add(db_connected)
    db.commit()
    db.refresh(db_connected)
    return db_connected

def get_linked_articles(db: Session, culture_id: int):
    return db.query(OtherArticleCulture).filter(OtherArticleCulture.id_culture == culture_id).all()

def delete_linked_article(db: Session, connected_id: int, culture_id: int):
    connected = db.query(OtherArticleCulture).filter(
        OtherArticleCulture.id == connected_id,
        OtherArticleCulture.id_culture == culture_id
    ).first()
    if not connected:
        return None
    db.delete(connected)
    db.commit()
    return connected