from domain.entities.user import User
from services.models.inputs.update_user_sim import UpdateUserSIM
from services.models.outputs.update_user_som import UpdateUserSOM


class UpdateUserMapper:
  @staticmethod
  def entity_to_som(entity: User) -> UpdateUserSOM:
    return UpdateUserSOM(
      uuid=entity.uuid,
      email_address=entity.email_address,
      username=entity.username
    )
