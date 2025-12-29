from datetime import datetime, timezone
from typing import ClassVar, Optional

from sqlmodel import Field, SQLModel


class MembershipORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "membership"
  ulid: str = Field(primary_key=True, max_length=26)
  account_ulid: str = Field(
    foreign_key="account.ulid",
    nullable=False,
    max_length=26
  )
  role_ulid: str = Field(
    foreign_key="role.ulid",
    nullable=False,
    max_length=26
  )
  user_ulid: str = Field(
    foreign_key="user.ulid",
    nullable=False,
    max_length=26
  )
  status: str = Field(
    nullable=False,
    max_length=16
  )
  joined_at: datetime = Field(
    default_factory=lambda: datetime.now(tz=timezone.utc),
    nullable=False
  )
  removed_at: Optional[datetime] = Field(default=None)
