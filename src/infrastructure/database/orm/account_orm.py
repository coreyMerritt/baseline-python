from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class AccountORM(SQLModel, table=True):
  id: int = Field(
    nullable=False,
    unique=True,
    primary_key=True,
    default=None
  )
  uuid: str = Field(
    nullable=False,
    unique=True,
    primary_key=False
  )
  name: str = Field(
    nullable=False,
    unique=False,
    primary_key=False
  )
  age: int = Field(
    nullable=False,
    unique=False,
    primary_key=False
  )
  account_type: str = Field(
    nullable=False,
    unique=False,
    primary_key=False
  )
  timestamp: datetime = Field(
    nullable=False,
    unique=False,
    primary_key=False,
    default_factory=lambda: datetime.now(timezone.utc)
  )
