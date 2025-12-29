from typing import ClassVar

from sqlmodel import Field, SQLModel


class RoleORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "role"
  ulid: str = Field(primary_key=True, max_length=26)
  name: str = Field(
    nullable=False,
    unique=True,
    max_length=64
  )
