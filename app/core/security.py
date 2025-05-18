from fastapi import Depends, HTTPException, status
from app.core.auth import get_current_admin
from app.database.models import AdminRole, Admin


class RoleChecker:
    def __init__(self, allowed_roles: list[AdminRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: Admin = Depends(get_current_admin)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )

allow_create_edit = RoleChecker([AdminRole.ADMIN])
