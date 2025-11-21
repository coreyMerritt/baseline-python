from domain.entities.account import Account
from services.models.outputs.get_account_som import GetAccountSOM


class GetAccountMapper:
  @staticmethod
  def account_to_som(account: Account) -> GetAccountSOM:
    return GetAccountSOM(
      uuid=account.uuid,
      name=account.name,
      age=account.age,
      account_type=account.account_type
    )
