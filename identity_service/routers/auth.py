from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from identity_service.config import get_current_settings
from identity_service.db import get_session
from identity_service.models import Token, User
from identity_service.utils.auth import create_access_token, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/basic", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    settings = get_current_settings()
    user_query = await session.exec(
        select(User).where(User.username == form_data.username)
    )
    user = user_query.one()
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not user:
        raise unauthorized_exception
    if not verify_password(user, form_data.password):
        # TODO: Exponential backoff and audit logging.
        raise unauthorized_exception
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.jwt_expiration_time_in_seconds),
    )
    return {"access_token": access_token, "token_type": "bearer"}
