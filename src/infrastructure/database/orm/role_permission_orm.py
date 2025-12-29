from typing import ClassVar

from sqlmodel import Field, SQLModel


class RolePermissionORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "role_permission"
  role_ulid: str = Field(
    foreign_key="role.ulid",
    primary_key=True,
    max_length=26
  )
  permission_ulid: str = Field(
    foreign_key="permission.ulid",
    primary_key=True,
    max_length=26
  )
