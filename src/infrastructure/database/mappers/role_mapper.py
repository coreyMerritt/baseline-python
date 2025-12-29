from domain.subdomain.entities.role import Role
from infrastructure.database.orm.role_orm import RoleORM


class RoleMapper:
  @staticmethod
  def domain_to_orm(role: Role) -> RoleORM:
    return RoleORM(
      ulid=role.ulid,
      name=role.name
    )

  @staticmethod
  def orm_to_domain(role_orm: RoleORM) -> Role:
    return Role(
      ulid=role_orm.ulid,
      name=role_orm.name
    )
