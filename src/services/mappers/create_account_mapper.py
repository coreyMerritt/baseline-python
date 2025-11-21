from domain.entities.account import Account
from services.models.inputs.create_account_sim import CreateAccountSIM
from services.models.outputs.create_account_som import CreateAccountSOM


class CreateAccountMapper:
  @staticmethod
  def sim_to_entity(sim: CreateAccountSIM) -> Account:
    return Account(
      uuid=sim.uuid,
      name=sim.name,
      age=sim.age,
      account_type=sim.account_type
    )

  @staticmethod
  def entity_to_som(entity: Account) -> CreateAccountSOM:
    return CreateAccountSOM(
      uuid=entity.uuid,
      name=entity.name,
      age=entity.age,
      account_type=entity.account_type
    )
