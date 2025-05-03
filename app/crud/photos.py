from sqlalchemy.orm import Session
from app.database.models import PhotoExhibit
from app.schemas.photos import PhotoCreate

def add_photo_to_exhibit(db: Session, exhibit_id: int, photo: PhotoCreate):
    db_photo = PhotoExhibit(
        photo=photo.photo,
        id_exhibit=exhibit_id
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def get_photos_for_exhibit(db: Session, exhibit_id: int):
    return db.query(PhotoExhibit).filter(PhotoExhibit.id_exhibit == exhibit_id).all()

def delete_photo(db: Session, photo_id: int, exhibit_id: int):
    photo = db.query(PhotoExhibit).filter(
        PhotoExhibit.id == photo_id,
        PhotoExhibit.id_exhibit == exhibit_id
    ).first()
    if not photo:
        return None
    db.delete(photo)
    db.commit()
    return photo