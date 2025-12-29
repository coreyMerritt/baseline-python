from domain.subdomain.entities.account import Account
from services.models.inputs.account.update_account_sim import UpdateAccountSIM
from services.models.outputs.account.update_account_som import UpdateAccountSOM


class UpdateAccountMapper:
  @staticmethod
  def sim_to_entity(old_entity: Account, sim: UpdateAccountSIM) -> Account:
    entity = old_entity
    entity.name = sim.name
    entity.status = sim.status
    return entity

  @staticmethod
  def entity_to_som(entity: Account) -> UpdateAccountSOM:
    return UpdateAccountSOM(
      ulid=entity.ulid,
      name=entity.name,
      status=entity.status,
      created_at=entity.created_at,
      suspended_at=entity.suspended_at,
      deleted_at=entity.deleted_at
    )
