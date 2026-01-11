from domain.interfaces.repositories.user_credential_repository_interface import UserCredentialRepositoryInterface
from domain.interfaces.repositories.user_repository_interface import UserRepositoryInterface
from infrastructure.auth.models.user_credential import UserCredential
from infrastructure.auth.password_hasher import PasswordHasher
from infrastructure.types.logger_interface import LoggerInterface
from services.base_service import BaseService
from services.mappers.user.create_user_mapper import CreateUserMapper
from services.mappers.user.delete_user_mapper import DeleteUserMapper
from services.mappers.user.get_user_mapper import GetUserMapper
from services.mappers.user.update_user_mapper import UpdateUserMapper
from services.models.inputs.user.create_user_sim import CreateUserSIM
from services.models.inputs.user.update_user_sim import UpdateUserSIM
from services.models.outputs.user.create_user_som import CreateUserSOM
from services.models.outputs.user.delete_user_som import DeleteUserSOM
from services.models.outputs.user.get_user_som import GetUserSOM
from services.models.outputs.user.update_user_som import UpdateUserSOM


class UserManager(BaseService):
  _password_hasher: PasswordHasher
  _user_repository: UserRepositoryInterface
  _user_credential_repository: UserCredentialRepositoryInterface

  def __init__(
    self,
    logger: LoggerInterface,
    password_hasher: PasswordHasher,
    user_repository: UserRepositoryInterface,
    user_credential_repository: UserCredentialRepositoryInterface
  ):
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
