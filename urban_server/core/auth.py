from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.database_queries import get_user_by_username
from core.databases import get_session
from core.models import User, generate_token

security = HTTPBasic()


async def get_current_user(
    db: AsyncSession = Depends(get_session),
    credentials: HTTPBasicCredentials = Depends(security),
) -> User:
    username, password = credentials.username, credentials.password

    if (
        user := await get_user_by_username(username, db)
    ) and user.token == generate_token(password):
        return user
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


async def get_available_user(user: User = Depends(get_current_user)):
    if user.available_requests > 0:
        return user
    else:
        raise HTTPException(status_code=403, detail="No free queries!")
