from domain.entities.account import Account
from domain.enums.account_type import AccountType
from domain.exceptions.validation_err import ValidationErr
from infrastructure.database.exceptions.database_insert_err import DatabaseInsertErr
from infrastructure.database.exceptions.database_select_err import DatabaseSelectErr
from services.base_database_aware_service import DatabaseAwareService
from services.exceptions.item_creation_err import ItemCreationErr
from services.exceptions.item_not_found_err import ItemNotFoundErr


class AccountManager(DatabaseAwareService):
  def get_account(self, uuid: str) -> Account | None:
    try:
      account = self._get_account_from_database(uuid)
    except DatabaseSelectErr as e:
      raise ItemNotFoundErr() from e
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
      raise ItemCreationErr() from e
    try:
      created_account = self._create_account_in_database(account)
    except DatabaseInsertErr as e:
      raise ItemCreationErr() from e
    return created_account

  def _get_account_from_database(
    self,
    uuid: str
  ) -> Account | None:
    self._logger.debug("Attempting to retrieve account for uuid: %s", uuid)
    account = self._database.get_account_from_uuid(uuid)
    self._logger.debug("Successfully retrieved account for uuid: %s", uuid)
    return account

  def _create_account_in_database(
    self,
    account: Account
  ) -> Account:
    self._logger.debug("Attempting to create account...")
    account = self._database.insert_account(account)
    self._logger.debug("Successfully created account for uuid: %s", account.get_uuid())
    return account
