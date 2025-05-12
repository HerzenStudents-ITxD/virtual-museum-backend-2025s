from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.auth import (
    create_access_token,
    verify_password,
    get_current_admin
)

from app.database.database import get_db
from app.database.models import Admin
from app.schemas.auth import Token

router = APIRouter(prefix="/api/auth")


@router.post("/login", response_model=Token, tags=["Авторизация"])
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.login == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.salt, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    access_token = create_access_token(data={"sub": admin.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", tags=["Авторизация"])
async def read_admin_me(current_admin: Admin = Depends(get_current_admin)):
    return {"login": current_admin.login}