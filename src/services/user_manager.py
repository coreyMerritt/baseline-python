from datetime import UTC, datetime
from domain.enums.membership_status import MembershipStatus
from domain.interfaces.repositories.membership_repository_interface import MembershipRepositoryInterface
from domain.interfaces.repositories.role_repository_interface import RoleRepositoryInterface
from domain.interfaces.repositories.user_credential_repository_interface import UserCredentialRepositoryInterface
from domain.interfaces.repositories.user_repository_interface import UserRepositoryInterface
from domain.subdomain.entities.membership import Membership
from infrastructure.auth.models.user_credential import UserCredential
from infrastructure.auth.password_hasher import PasswordHasher
from infrastructure.types.logger_interface import LoggerInterface
from services.account_manager import AccountManager
from services.base_service import BaseService
from services.mappers.user.create_user_mapper import CreateUserMapper
from services.mappers.user.delete_user_mapper import DeleteUserMapper
from services.mappers.user.get_user_mapper import GetUserMapper
from services.mappers.user.update_user_mapper import UpdateUserMapper
from services.models.inputs.account.create_account_sim import CreateAccountSIM
from services.models.inputs.user.create_user_sim import CreateUserSIM
from services.models.inputs.user.update_user_sim import UpdateUserSIM
from services.models.outputs.user.create_user_som import CreateUserSOM
from services.models.outputs.user.delete_user_som import DeleteUserSOM
from services.models.outputs.user.get_user_som import GetUserSOM
from services.models.outputs.user.update_user_som import UpdateUserSOM


class UserManager(BaseService):
  _account_manager: AccountManager
  _password_hasher: PasswordHasher
  _membership_repository: MembershipRepositoryInterface
  _role_repository: RoleRepositoryInterface
  _user_repository: UserRepositoryInterface
  _user_credential_repository: UserCredentialRepositoryInterface

  def __init__(
    self,
    logger: LoggerInterface,
    account_manager: AccountManager,
    membership_repository: MembershipRepositoryInterface,
    role_repository: RoleRepositoryInterface,
    password_hasher: PasswordHasher,
    user_repository: UserRepositoryInterface,
    user_credential_repository: UserCredentialRepositoryInterface
  ):
    self._account_manager = account_manager
    self._membership_repository = membership_repository
    self._role_repository = role_repository
    self._password_hasher = password_hasher
    self._user_repository = user_repository
    self._user_credential_repository = user_credential_repository
    super().__init__(logger)

  def create_user(self, create_user_sim: CreateUserSIM) -> CreateUserSOM:
    self._logger.debug("Attempting to create user...")
    user = CreateUserMapper.sim_to_entity(create_user_sim)
    try:
      created_user = self._user_repository.create(user)
      password_hash = self._password_hasher.hash(create_user_sim.password)
      self._user_credential_repository.create(
        UserCredential(
          user_ulid=created_user.ulid,
          password_hash=password_hash
        )
      )
      created_account = self._account_manager.create_account(
        CreateAccountSIM(
          name=create_user_sim.username
        )
      )
      owner_role = self._role_repository.get_by_name("account_owner")
      assert owner_role.ulid
      self._membership_repository.create(Membership(
        ulid=None,
        user_ulid=created_user.ulid,
        account_ulid=created_account.ulid,
        role_ulid=owner_role.ulid,
        status=MembershipStatus.ACTIVE,
        joined_at=datetime.now(tz=UTC),
        removed_at=None
      ))
    except Exception as e:
      self._raise_service_exception(e)
    create_user_som = CreateUserMapper.entity_to_som(created_user)
    self._logger.debug(f"Successfully created user with ULID: {created_user.ulid}")
    return create_user_som

  def get_user(self, ulid: str) -> GetUserSOM:
    self._logger.debug(f"Attempting to retrieve user with ULID: {ulid}")
    try:
      user = self._user_repository.get(ulid)
    except Exception as e:
      self._raise_service_exception(e)
    get_user_som = GetUserMapper.entity_to_som(user)
    self._logger.debug(f"Successfully retrieved user with ULID: {ulid}")
    return get_user_som

  def update_user(self, update_user_sim: UpdateUserSIM) -> UpdateUserSOM:
    self._logger.debug("Attempting to update user...")
    pre_changes_user = self._user_repository.get(update_user_sim.ulid)
    user = UpdateUserMapper.sim_to_entity(pre_changes_user, update_user_sim)
    try:
      user = self._user_repository.update(user)
    except Exception as e:
      self._raise_service_exception(e)
    get_user_som = UpdateUserMapper.entity_to_som(user)
    self._logger.debug(f"Successfully retrieved user with ULID: {user.ulid}")
    return get_user_som

  def delete_user(self, ulid: str) -> DeleteUserSOM:
    self._logger.debug(f"Attempting to retrieve user with ULID: {ulid}")
    try:
      user = self._user_repository.delete(ulid)
    except Exception as e:
      self._raise_service_exception(e)
    delete_user_som = DeleteUserMapper.entity_to_som(user)
    self._logger.debug(f"Successfully retrieved user with ULID: {ulid}")
    return delete_user_som
