from fastapi import Depends, HTTPException, status
from backend.src.core.auth.current import get_current_user
from backend.src.core.auth.models import User
from backend.src.core.models.role import Role


def require_role(min_role: Role):
    async def check_role(user: User = Depends(get_current_user)):
        if user.role > min_role:  # Меньше значение — выше привилегии
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return user

    return check_role
