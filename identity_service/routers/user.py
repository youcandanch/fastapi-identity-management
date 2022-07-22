from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from identity_service.db import get_session
from identity_service.models import TokenData, User, UserCreate, UserRead
from identity_service.utils.auth import get_password_hash, get_token_data

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/me/", response_model=UserRead)
async def get_current_user(
    token_data: TokenData = Depends(get_token_data),
    session: AsyncSession = Depends(get_session),
):
    user_query = await session.exec(
        select(User).where(User.username == token_data.username)
    )
    user = user_query.one()
    return user


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User.from_orm(user)
    user.password = get_password_hash(user.password)
    session.add(user)
    await session.commit()
    session.refresh(user)
    return user
