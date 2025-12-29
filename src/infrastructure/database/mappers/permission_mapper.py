from domain.subdomain.entities.permission import Permission
from infrastructure.database.orm.permission_orm import PermissionORM


class PermissionMapper:
  @staticmethod
  def domain_to_orm(permission: Permission) -> PermissionORM:
    return PermissionORM(
      ulid=permission.ulid,
      key=permission.key
    )

  @staticmethod
  def orm_to_domain(permission_orm: PermissionORM) -> Permission:
    return Permission(
      ulid=permission_orm.ulid,
      key=permission_orm.key
    )
