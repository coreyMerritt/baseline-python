from domain.subdomain.entities.account import Account
from services.models.inputs.account.create_account_sim import CreateAccountSIM
from services.models.outputs.account.create_account_som import CreateAccountSOM


class CreateAccountMapper:
  @staticmethod
  def sim_to_entity(sim: CreateAccountSIM) -> Account:
    return Account(
      name=sim.name,
      ulid=None,
      status=None,
      created_at=None,
      suspended_at=None,
      deleted_at=None
    )

  @staticmethod
  def entity_to_som(entity: Account) -> CreateAccountSOM:
    return CreateAccountSOM(
      ulid=entity.ulid,
      name=entity.name,
      status=entity.status,
      created_at=entity.created_at,
      suspended_at=entity.suspended_at,
      deleted_at=entity.deleted_at
    )
