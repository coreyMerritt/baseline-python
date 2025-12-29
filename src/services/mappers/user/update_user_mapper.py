from domain.subdomain.entities.user import User
from services.models.inputs.user.update_user_sim import UpdateUserSIM
from services.models.outputs.user.update_user_som import UpdateUserSOM


class UpdateUserMapper:
  @staticmethod
  def sim_to_entity(old_entity: User, sim: UpdateUserSIM) -> User:
    entity = old_entity
    entity.username = sim.username
    entity.email_address = sim.email_address
    entity.email_verified = sim.email_verified
    if sim.disabled:
      entity.disable()
    else:
      entity.enable()
    return entity

  @staticmethod
  def entity_to_som(entity: User) -> UpdateUserSOM:
    return UpdateUserSOM(
      ulid=entity.ulid,
      email_address=entity.email_address,
      username=entity.username
    )
