from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class UserORM(SQLModel, table=True):
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
  external_mapping_id: str = Field(
    nullable=False,
    unique=True,
    primary_key=False
  )
  email_address: str = Field(
    nullable=False,
    unique=True,
    primary_key=False
  )
  username: str = Field(
    nullable=False,
    unique=True,
    primary_key=False
  )
  timestamp: datetime = Field(
    nullable=False,
    unique=False,
    primary_key=False,
    default_factory=lambda: datetime.now(timezone.utc)
  )
