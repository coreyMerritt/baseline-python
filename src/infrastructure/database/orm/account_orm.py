from datetime import datetime, timezone
from typing import ClassVar, Optional

from sqlmodel import Field, SQLModel


class AccountORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "account"
  ulid: str = Field(primary_key=True, max_length=26)
  name: str = Field(nullable=False, max_length=128)
  status: str = Field(
    nullable=False,
    max_length=16
  )
  created_at: datetime = Field(
    default_factory=lambda: datetime.now(tz=timezone.utc),
    nullable=False
  )
  suspended_at: Optional[datetime] = Field(default=None)
  deleted_at: Optional[datetime] = Field(default=None)
