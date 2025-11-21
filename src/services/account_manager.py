from domain.interfaces.repositories.account_repository_interface import AccountRepositoryInterface
from services.base_service import BaseService
from services.mappers.create_account_mapper import CreateAccountMapper
from services.mappers.get_account_mapper import GetAccountMapper
from services.models.inputs.create_account_sim import CreateAccountSIM
from services.models.outputs.create_account_som import CreateAccountSOM
from services.models.outputs.get_account_som import GetAccountSOM
from shared.types.logger_interface import LoggerInterface


class AccountManager(BaseService):
  _account_repository: AccountRepositoryInterface

  def __init__(self, logger: LoggerInterface, account_repository: AccountRepositoryInterface):
    self._account_repository = account_repository
    super().__init__(logger)

  def create_account(self, create_account_sim: CreateAccountSIM) -> CreateAccountSOM:
    self._logger.debug("Attempting to create account...")
    account = CreateAccountMapper.sim_to_entity(create_account_sim)
    try:
      created_account = self._account_repository.insert(account)
    except Exception as e:
      self._raise_service_exception(e)
    create_account_som = CreateAccountMapper.entity_to_som(created_account)
    self._logger.debug("Successfully created account for uuid: %s", account.uuid)
    return create_account_som

  def get_account(self, uuid: str) -> GetAccountSOM:
    self._logger.debug("Attempting to retrieve account for uuid: %s", uuid)
    try:
      account = self._account_repository.get(uuid)
    except Exception as e:
      self._raise_service_exception(e)
    get_account_som = GetAccountMapper.account_to_som(account)
    self._logger.debug("Successfully retrieved account for uuid: %s", uuid)
    return get_account_som
