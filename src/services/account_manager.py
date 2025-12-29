from domain.enums.membership_status import MembershipStatus
from domain.interfaces.repositories.account_repository_interface import AccountRepositoryInterface
from infrastructure.database.repositories.membership_repository import MembershipRepository
from infrastructure.database.repositories.role_repository import RoleRepository
from infrastructure.types.logger_interface import LoggerInterface
from services.base_service import BaseService
from services.exceptions.account_deleted_err import AccountDeletedErr
from services.exceptions.account_suspended_err import AccountSuspendedErr
from services.mappers.account.create_account_mapper import CreateAccountMapper
from services.mappers.account.delete_account_mapper import DeleteAccountMapper
from services.mappers.account.get_account_mapper import GetAccountMapper
from services.mappers.account.update_account_mapper import UpdateAccountMapper
from services.models.inputs.account.create_account_sim import CreateAccountSIM
from services.models.inputs.account.update_account_sim import UpdateAccountSIM
from services.models.outputs.account.create_account_som import CreateAccountSOM
from services.models.outputs.account.delete_account_som import DeleteAccountSOM
from services.models.outputs.account.get_account_som import GetAccountSOM
from services.models.outputs.account.update_account_som import UpdateAccountSOM


class AccountManager(BaseService):
  _account_repository: AccountRepositoryInterface
  _membership_repository: MembershipRepository
  _role_repository: RoleRepository

  def __init__(
    self,
    logger: LoggerInterface,
    account_repository: AccountRepositoryInterface,
    membership_repository: MembershipRepository,
    role_repository: RoleRepository
  ):
    self._account_repository = account_repository
    self._membership_repository = membership_repository
    self._role_repository = role_repository
    super().__init__(logger)

  def create_account(self, create_account_sim: CreateAccountSIM) -> CreateAccountSOM:
    self._logger.debug("Attempting to create account...")
    account = CreateAccountMapper.sim_to_entity(create_account_sim)
    try:
      created_account = self._account_repository.create(account)
    except Exception as e:
      self._raise_service_exception(e)
    create_account_som = CreateAccountMapper.entity_to_som(created_account)
    self._logger.debug(f"Successfully created account for ulid: {account.ulid}")
    return create_account_som

  def get_account(self, ulid: str) -> GetAccountSOM:
    self._logger.debug(f"Attempting to retrieve account for ulid: {ulid}")
    try:
      account = self._account_repository.get(ulid)
    except Exception as e:
      self._raise_service_exception(e)
    get_account_som = GetAccountMapper.entity_to_som(account)
    self._logger.debug(f"Successfully retrieved account for ulid: {ulid}")
    return get_account_som

  def update_account(self, update_account_sim: UpdateAccountSIM) -> UpdateAccountSOM:
    self._logger.debug("Attempting to update account...")
    pre_changes_account = self._account_repository.get(update_account_sim.ulid)
    account = UpdateAccountMapper.sim_to_entity(pre_changes_account, update_account_sim)
    try:
      account = self._account_repository.update(account)
    except Exception as e:
      self._raise_service_exception(e)
    get_account_som = UpdateAccountMapper.entity_to_som(account)
    self._logger.debug(f"Successfully retrieved account for ulid: {account.ulid}")
    return get_account_som

  def delete_account(self, ulid: str) -> DeleteAccountSOM:
    self._logger.debug(f"Attempting to retrieve account for ulid: {ulid}")
    try:
      account = self._account_repository.delete(ulid)
    except Exception as e:
      self._raise_service_exception(e)
    delete_account_som = DeleteAccountMapper.entity_to_som(account)
    self._logger.debug(f"Successfully retrieved account for ulid: {ulid}")
    return delete_account_som

  # def invite_member(self, invite_member_sim: InviteMemberSIM) -> InviteMemberSOM:
  #   self._logger.debug(
  #     f"Inviting user {invite_member_sim.user_ulid} "
  #     f"to account {invite_member_sim.account_ulid}"
  #   )
  #   account = self._account_repository.get(invite_member_sim.account_ulid)
  #   if account.deleted_at is not None:
  #     raise AccountDeletedErr()
  #   if account.suspended_at is not None:
  #     raise AccountSuspendedErr()
  #   role = self._role_repository.get(invite_member_sim.role_ulid)
  #   membership = InviteMemberMapper.sim_to_entity(
  #     invite_member_sim=invite_member_sim,
  #     status=MembershipStatus.INVITED,
  #     joined_at=None,
  #     removed_at=None,
  #   )
  #   try:
  #     membership = self._membership_repository.create(membership)
  #   except Exception as e:
  #     self._raise_service_exception(e)
  #   return InviteMemberMapper.entity_to_som(membership)

  # def accept_member_invite(self, membership_ulid: str) -> AcceptMemberInviteSOM:
  #   self._logger.debug(f"Accepting membership invite {membership_ulid}")
  #   membership = self._membership_repository.get(membership_ulid)
  #   if membership.status != MembershipStatus.INVITED:
  #     raise ValueError("Only invited memberships can be accepted")
  #   membership.status = MembershipStatus.ACTIVE
  #   membership.joined_at = datetime.now(tz=timezone.utc)
  #   try:
  #     membership = self._membership_repository.update(membership)
  #   except Exception as e:
  #     self._raise_service_exception(e)
  #   return AcceptMemberInviteMapper.entity_to_som(membership)

  # def change_member_role(
  #   self,
  #   account_ulid: str,
  #   membership_ulid: str,
  #   new_role_ulid: str,
  # ) -> ChangeMemberRoleSOM:
  #   self._logger.debug(
  #     f"Changing role for membership {membership_ulid} "
  #     f"on account {account_ulid}"
  #   )
  #   account = self._account_repository.get(account_ulid)
  #   membership = self._membership_repository.get(membership_ulid)
  #   if membership.account_ulid != account.ulid:
  #     raise ValueError("Membership does not belong to account")
  #   role = self._role_repository.get(new_role_ulid)
  #   membership.role_ulid = role.ulid
  #   try:
  #     membership = self._membership_repository.update(membership)
  #   except Exception as e:
  #     self._raise_service_exception(e)
  #   return ChangeMemberRoleMapper.entity_to_som(membership)

  # def remove_member(
  #   self,
  #   account_ulid: str,
  #   membership_ulid: str,
  # ) -> RemoveMemberSOM:
  #   self._logger.debug(
  #     f"Removing membership {membership_ulid} "
  #     f"from account {account_ulid}"
  #   )
  #   account = self._account_repository.get(account_ulid)
  #   membership = self._membership_repository.get(membership_ulid)
  #   if membership.account_ulid != account.ulid:
  #     raise ValueError("Membership does not belong to account")
  #   if membership.status == MembershipStatus.REMOVED:
  #     raise ValueError("Membership already removed")
  #   membership.status = MembershipStatus.REMOVED
  #   membership.removed_at = datetime.now(tz=timezone.utc)
  #   try:
  #     membership = self._membership_repository.update(membership)
  #   except Exception as e:
  #     self._raise_service_exception(e)
  #   return RemoveMemberMapper.entity_to_som(membership)
