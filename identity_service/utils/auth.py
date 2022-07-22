from datetime import datetime, timedelta
from functools import lru_cache

from jose import jwt
from passlib.context import CryptContext

from identity_service.config import get_current_settings
from identity_service.models import TokenData


@lru_cache()
def _get_password_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    settings = get_current_settings()
    encoded_jwt = jwt.encode(
        to_encode,
        settings.password_hash_secret_key,
        algorithm=settings.password_hash_algorithm,
    )
    return encoded_jwt


async def get_token_data(token: str) -> TokenData:
    settings = get_current_settings()
    payload = jwt.decode(
        token,
        settings.password_hash_secret_key,
        algorithms=[settings.password_hash_algorithm],
    )
    username: str = payload.get("sub")
    if username is None:
        raise Exception("No username in token.")
    token_data = TokenData(username=username)
    return token_data


def get_password_hash(password):
    return _get_password_context().hash(password)


def verify_password(user, plain_password):
    return _get_password_context().verify(plain_password, user.password)
