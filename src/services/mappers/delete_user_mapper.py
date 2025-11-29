from domain.entities.user import User
from services.models.outputs.delete_user_som import DeleteUserSOM


class DeleteUserMapper:
  @staticmethod
  def entity_to_som(entity: User) -> DeleteUserSOM:
    return DeleteUserSOM(
      uuid=entity.uuid,
      email_address=entity.email_address,
      username=entity.username
    )
