from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

# from .databases import Base
from .models import User


async def get_user_by_username(username: str, db: AsyncSession) -> User:
    query = select(User).where(User.username == username)
    return (await db.scalars(query)).first()
