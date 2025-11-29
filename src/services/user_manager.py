# from domain.entities.user import User
# from domain.interfaces.repositories.user_repository_interface import UserRepositoryInterface
# from domain.validators.email_address import EmailValidator
# from infrastructure.external_services.models.external_services_config import ExternalServicesConfig
# from infrastructure.types.logger_interface import LoggerInterface
# from services.base_service import BaseService
# from services.mappers.create_user_mapper import CreateUserMapper
# from services.mappers.get_user_mapper import GetUserMapper
# from services.models.inputs.create_user_sim import CreateUserSIM
# from services.models.outputs.create_user_som import CreateUserSOM
# from services.models.outputs.delete_user_som import DeleteUserSOM
# from services.models.outputs.get_user_som import GetUserSOM
# from services.models.outputs.update_user_som import UpdateUserSOM


# class UserManager(BaseService):
#   _user_repository: UserRepositoryInterface

#   def __init__(self,
#     logger: LoggerInterface,
#     user_repository: UserRepositoryInterface,
#     external_services_config: ExternalServicesConfig
#   ):
#     self._user_repository = user_repository
#     super().__init__(logger)

#   def create_user(self, create_user_sim: CreateUserSIM) -> CreateUserSOM:
#     self._logger.debug("Attempting to create user...")
#     EmailValidator.validate(create_user_sim.email_address)
#     external_mapping_id = self._entra_id_client.create_user(
#       username=create_user_sim.username,
#       password=create_user_sim.password,
#       token=None
#     )
#     user = User(
#       uuid=None,
#       external_mapping_id=external_mapping_id,
#       email_address=create_user_sim.email_address,
#       username=create_user_sim.username
#     )
#     created_user = self._user_repository.create(user)
#     create_user_som = CreateUserMapper.entity_to_som(created_user)
#     self._logger.debug(f"Successfully created user for uuid: {user.uuid}")
#     return create_user_som

#   def get_user(self, uuid: str) -> GetUserSOM:
#     self._logger.debug(f"Attempting to retrieve user for uuid: {uuid}")
#     try:
#       user = self._user_repository.get(uuid)
#     except Exception as e:
#       self._raise_service_exception(e)
#     get_user_som = GetUserMapper.user_to_som(user)
#     self._logger.debug(f"Successfully retrieved user for uuid: {uuid}")
#     return get_user_som

#   def update_user(self, update_user_sim: UpdateUserSIM) -> UpdateUserSOM:
#     ...

#   def delete_user(self, uuid: str) -> DeleteUserSOM:
#     ...
