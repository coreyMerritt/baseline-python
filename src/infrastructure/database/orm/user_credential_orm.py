from datetime import datetime, timezone
from typing import ClassVar

from sqlmodel import Field, SQLModel


class UserCredentialORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "user_credential"
  user_ulid: str = Field(
    foreign_key="user.ulid",
    primary_key=True,
    max_length=26,
  )
  password_hash: str = Field(
    nullable=False,
    max_length=255,
  )
  created_at: datetime = Field(
    default_factory=lambda: datetime.now(tz=timezone.utc),
    nullable=False,
  )
