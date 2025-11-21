from domain.entities.account import Account
from domain.exceptions.validation_err import ValidationErr
from infrastructure.database.exceptions.database_insert_err import DatabaseInsertErr
from infrastructure.database.exceptions.database_select_err import DatabaseSelectErr
from infrastructure.database.exceptions.zero_query_results_err import ZeroQueryResultsErr
from services.base_database_aware_service import DatabaseAwareService
from services.exceptions.item_creation_err import ItemCreationErr
from services.exceptions.item_not_found_err import ItemNotFoundErr
from services.mappers.create_account_mapper import CreateAccountMapper
from services.mappers.get_account_mapper import GetAccountMapper
from services.models.inputs.create_account_sim import CreateAccountSIM
from services.models.outputs.create_account_som import CreateAccountSOM
from services.models.outputs.get_account_som import GetAccountSOM


class AccountManager(DatabaseAwareService):
  def create_account(self, create_account_sim: CreateAccountSIM) -> CreateAccountSOM:
    try:
      account = Account(
        name=create_account_sim.name,
        age=create_account_sim.age,
        account_type=create_account_sim.account_type
      )
    except ValidationErr as e:
      raise ItemCreationErr() from e
    try:
      created_account = self._create_account_in_database(account)
    except DatabaseInsertErr as e:
      raise ItemCreationErr() from e
    create_account_som = CreateAccountMapper.account_to_som(created_account)
    return create_account_som

  def get_account(self, uuid: str) -> GetAccountSOM:
    try:
      account = self._get_account_from_database(uuid)
    except DatabaseSelectErr as e:
      raise ItemNotFoundErr() from e
    except ZeroQueryResultsErr as e:
      raise ItemNotFoundErr() from e
    get_account_som = GetAccountMapper.account_to_som(account)
    return get_account_som

  def _create_account_in_database(
    self,
    account: Account
  ) -> Account:
    self._logger.debug("Attempting to create account...")
    account = self._database.insert_account(account)
    self._logger.debug("Successfully created account for uuid: %s", account.get_uuid())
    return account

  def _get_account_from_database(
    self,
    uuid: str
  ) -> Account:
    self._logger.debug("Attempting to retrieve account for uuid: %s", uuid)
    account = self._database.get_account_from_uuid(uuid)
    self._logger.debug("Successfully retrieved account for uuid: %s", uuid)
    return account
