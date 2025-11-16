from domain.entities.account import Account
from domain.enums.account_type import AccountType
from domain.exceptions.validation_err import ValidationErr
from infrastructure.database.exceptions.database_select_err import DatabaseSelectErr
from services.abc_database_aware_service import DatabaseAwareService
from services.exceptions.database_err import DatabaseErr
from services.exceptions.invalid_input_err import InvalidInputErr


class AccountManager(DatabaseAwareService):
  def get_account(self, uuid: str) -> Account | None:
    try:
      account = self._database_manager.get_account(uuid)
    except DatabaseSelectErr as e:
      raise DatabaseErr(str(e)) from e
    return account

  def create_account(self, uuid: str, name: str,age: int, account_type: AccountType) -> Account | None:
    try:
      account = Account(
        uuid=uuid,
        name=name,
        age=age,
        account_type=account_type
      )
    except ValidationErr as e:
      raise InvalidInputErr(str(e)) from e
    try:
      created_account = self._database_manager.create_account(account)
    except DatabaseSelectErr as e:
      raise DatabaseErr(str(e)) from e
    return created_account
