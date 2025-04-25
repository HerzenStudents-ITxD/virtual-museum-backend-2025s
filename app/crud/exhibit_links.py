from sqlalchemy.orm import Session
from app.database.models import OtherExhibit
from app.schemas.exhibit_links import ConnectedExhibitCreate

"""
linked_exhibit_id - id присоёдиненного экспоната
id_exhibit - id экспоната, к которому присоединяют
exhibit_id - то же что id_exhibit, но передаётся при запросе и вводится пользователем
"""


def add_connected_to_exhibit(db: Session, connected: ConnectedExhibitCreate):
    db_connected = OtherExhibit(**connected.model_dump())
    db.add(db_connected)
    db.commit()
    db.refresh(db_connected)
    return db_connected

def get_linked_exhibits(db: Session, exhibit_id: int):
    return db.query(OtherExhibit).filter(OtherExhibit.id_exhibit == exhibit_id).all()

def delete_linked_exhibit(db: Session, connected_id: int, exhibit_id: int):
    connected = db.query(OtherExhibit).filter(
        OtherExhibit.id == connected_id,
        OtherExhibit.id_exhibit == exhibit_id
    ).first()
    if not connected:
        return None
    db.delete(connected)
    db.commit()
    return connected