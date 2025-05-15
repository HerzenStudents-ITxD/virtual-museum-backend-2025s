import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models
from typing import Literal
from uuid import uuid4
from starlette.responses import JSONResponse

router = APIRouter(
    prefix="/api/photos",
    tags=["photos"]
)

UPLOAD_DIR = "uploads/images"


@router.post("/{type}/{item_id}")
def upload_photo(
    type: Literal["culture", "exhibit"],
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{uuid4().hex}_{file.filename}"
    folder = os.path.join(UPLOAD_DIR, type)
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as image:
        image.write(file.file.read())

    if type == "culture":
        culture = db.query(models.Culture).filter_by(id=item_id).first()
        if not culture:
            raise HTTPException(status_code=404, detail="Культура не найдена")

        # Обновляем поле main_photo в модели Culture
        culture.main_photo = file_path
        db.commit()

    elif type == "exhibit":
        exhibit = db.query(models.Exhibit).filter_by(id=item_id).first()
        if not exhibit:
            raise HTTPException(status_code=404, detail="Экспонат не найден")

        # Обновляем поле main_photo в модели Exhibit
        exhibit.main_photo = file_path
        db.commit()

    return {"message": "Фото успешно загружено", "path": file_path}


@router.delete("/{type}/{item_id}")
def delete_photo(
    type: Literal["culture", "exhibit"],
    item_id: int,
    db: Session = Depends(get_db)
):
    if type == "culture":
        culture = db.query(models.Culture).filter_by(id=item_id).first()
        if not culture:
            raise HTTPException(status_code=404, detail="Культура не найдена")

        if culture.main_photo and os.path.exists(culture.main_photo):
            os.remove(culture.main_photo)

        culture.main_photo = None
        db.commit()

    elif type == "exhibit":
        exhibit = db.query(models.Exhibit).filter_by(id=item_id).first()
        if not exhibit:
            raise HTTPException(status_code=404, detail="Экспонат не найден")

        if exhibit.main_photo and os.path.exists(exhibit.main_photo):
            os.remove(exhibit.main_photo)

        exhibit.main_photo = None
        db.commit()

    else:
        raise HTTPException(status_code=400, detail="Неверный тип")

    return {"message": "Фото успешно удалено"}

@router.get("/{type}/{item_id}")
def get_photos(
    type: Literal["culture", "exhibit"],
    item_id: int,
    db: Session = Depends(get_db)
):
    if type == "culture":
        culture = db.query(models.Culture).filter_by(id=item_id).first()
        if not culture:
            raise HTTPException(status_code=404, detail="Культура не найдена")
        
        return {"id": culture.id, "path": culture.main_photo}

    elif type == "exhibit":
        exhibit = db.query(models.Exhibit).filter_by(id=item_id).first()
        if not exhibit:
            raise HTTPException(status_code=404, detail="Экспонат не найден")

        return {"id": exhibit.id, "path": exhibit.main_photo}

    else:
        raise HTTPException(status_code=400, detail="Неверный тип")
