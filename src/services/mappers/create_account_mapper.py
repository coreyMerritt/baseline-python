from domain.entities.account import Account
from services.models.outputs.create_account_som import CreateAccountSOM


class CreateAccountMapper:
  @staticmethod
  def account_to_som(account: Account) -> CreateAccountSOM:
    return CreateAccountSOM(
      uuid=account.get_uuid(),
      name=account.get_name(),
      age=account.get_age(),
      account_type=account.get_account_type()
    )
