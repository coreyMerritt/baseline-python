from domain.entities.user import User
from services.exceptions.service_unavailable_err import ServiceUnavailableErr
from services.models.outputs.create_user_som import CreateUserSOM


class CreateUserMapper:
  @staticmethod
  def entity_to_som(entity: User) -> CreateUserSOM:
    if not entity.uuid:
      raise ServiceUnavailableErr()
    return CreateUserSOM(
      uuid=entity.uuid,
      email_address=entity.email_address,
      username=entity.username
    )
