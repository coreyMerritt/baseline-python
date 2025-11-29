from domain.entities.user import User
from services.models.outputs.get_user_som import GetUserSOM


class GetUserMapper:
  @staticmethod
  def entity_to_som(entity: User) -> GetUserSOM:
    return GetUserSOM(
      uuid=entity.uuid,
      email_address=entity.email_address,
      username=entity.username
    )
