from os import stat

import core.schemas as schemas
from core.auth import get_current_user
from core.database_queries import get_user_by_username
from core.databases import get_session
from core.models import User, generate_token
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users")


@router.post("/signup")
async def login(user_data: schemas.LoginInput, db: AsyncSession = Depends(get_session)):
    if await get_user_by_username(user_data.username, db):
        raise HTTPException(status_code=404, detail="User already exist!")

    user = User(username=user_data.username, token=generate_token(user_data.password))

    db.add(user)
    await db.commit()
    return Response(status_code=201)


@router.get("/me", response_model=schemas.AboutUserResponse)
async def about_me(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)
):
    return {
        "subscription": user.subscription_type,
        "available_requests": user.available_requests,
    }


@router.post("/bonus_by_token", response_model=schemas.BonusResponse)
async def bonus_by_token(
    token: schemas.BonusInput,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if token.password == "urban_bonus":
        user.subscription_type = "basic"
        user.available_requests += 10
        await db.commit()

        return {"content": "You win +10 queries!"}
    else:
        raise HTTPException(status_code=400, detail="Wrong token!")
