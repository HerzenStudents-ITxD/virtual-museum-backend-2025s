from sqlalchemy.orm import Session
import secrets

from app.core.auth import get_password_hash, verify_password
from app.database.models import Admin
from app.schemas.auth import AdminCreate

def create_admin(db: Session, admin: AdminCreate):
    """Создание нового администратора"""
    salt = secrets.token_hex(16)
    db_admin = Admin(
        login=admin.login,
        password_hash=get_password_hash(admin.password, salt),
        salt=salt,
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def authenticate_admin(db: Session, login: str, password: str):
    """Аутентификация администратора"""
    admin = db.query(Admin).filter(Admin.login == login).first()
    if not admin:
        return None
    if not verify_password(password, admin.salt, admin.password_hash):
        return None
    return admin