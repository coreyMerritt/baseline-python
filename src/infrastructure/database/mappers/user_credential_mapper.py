from infrastructure.auth.models.user_credential import UserCredential
from infrastructure.database.orm.user_credential_orm import UserCredentialORM


class UserCredentialMapper:
  @staticmethod
  def model_to_orm(user_credential: UserCredential) -> UserCredentialORM:
    return UserCredentialORM(
      user_ulid=user_credential.user_ulid,
      password_hash=user_credential.password_hash
    )

  @staticmethod
  def orm_to_model(user_orm: UserCredentialORM) -> UserCredential:
    return UserCredential(
      user_ulid=user_orm.user_ulid,
      password_hash=user_orm.password_hash
    )
