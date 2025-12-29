from domain.subdomain.entities.user import User
from services.exceptions.service_unavailable_err import ServiceUnavailableErr
from services.models.inputs.user.create_user_sim import CreateUserSIM
from services.models.outputs.user.create_user_som import CreateUserSOM


class CreateUserMapper:
  @staticmethod
  def sim_to_entity(sim: CreateUserSIM) -> User:
    return User(
      username=sim.username,
      email_address=sim.email_address,
      ulid=None,
      email_verified=None,
      created_at=None,
      disabled_at=None
    )

  @staticmethod
  def entity_to_som(entity: User) -> CreateUserSOM:
    if not entity.ulid:
      raise ServiceUnavailableErr()
    return CreateUserSOM(
      ulid=entity.ulid,
      email_address=entity.email_address,
      username=entity.username
    )
