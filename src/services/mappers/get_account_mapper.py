from domain.entities.account import Account
from services.models.outputs.get_account_som import GetAccountSOM


class GetAccountMapper:
  @staticmethod
  def account_to_som(account: Account) -> GetAccountSOM:
    return GetAccountSOM(
      uuid=account.get_uuid(),
      name=account.get_name(),
      age=account.get_age(),
      account_type=account.get_account_type()
    )
