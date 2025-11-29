from domain.entities.user import User
from infrastructure.database.orm.user_orm import UserORM


class UserMapper:
  @staticmethod
  def domain_to_orm(user: User) -> UserORM:
    return UserORM(
      uuid=user.uuid,
      external_mapping_id=user.external_mapping_id,
      email_address=user.email_address,
      username=user.username
    )

  @staticmethod
  def orm_to_domain(user_orm: UserORM) -> User:
    return User(
      uuid=user_orm.uuid,
      external_mapping_id=user_orm.external_mapping_id,
      email_address=user_orm.email_address,
      username=user_orm.username
    )
