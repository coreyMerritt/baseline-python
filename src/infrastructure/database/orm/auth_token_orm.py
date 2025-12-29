from datetime import datetime, timezone
from typing import ClassVar, Optional

from sqlmodel import Field, SQLModel


class AuthTokenORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "auth_token"
  ulid: str = Field(primary_key=True, max_length=26)
  user_ulid: str = Field(
    foreign_key="user.ulid",
    nullable=False,
    max_length=26
  )
  account_ulid: str = Field(
    foreign_key="account.ulid",
    nullable=False,
    max_length=26
  )
  token_hash: str = Field(
    nullable=False,
    max_length=255
  )
  expires_at: Optional[datetime] = Field(default=None)
  revoked_at: Optional[datetime] = Field(default=None)
  created_at: datetime = Field(
    default_factory=lambda: datetime.now(tz=timezone.utc),
    nullable=False
  )
