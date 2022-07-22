from datetime import datetime
from typing import Optional

import cuid
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: str = Field(default_factory=cuid.cuid, primary_key=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    date_modified: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            "date_modified",
            DateTime(timezone=False),
            nullable=False,
            onupdate=func.utcnow(),
        ),
    )


class UserCreate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserRead(SQLModel):
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    date_created: datetime
    date_modified: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
