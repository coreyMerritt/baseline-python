from typing import ClassVar

from sqlmodel import Field, SQLModel


class PermissionORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "permission"
  ulid: str = Field(primary_key=True, max_length=26)
  key: str = Field(
    nullable=False,
    unique=True,
    max_length=128
  )
