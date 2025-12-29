from domain.enums.membership_status import MembershipStatus
from domain.subdomain.entities.membership import Membership
from infrastructure.database.orm.membership_orm import MembershipORM


class MembershipMapper:
  @staticmethod
  def domain_to_orm(membership: Membership) -> MembershipORM:
    status_str = membership.status.value
    return MembershipORM(
      ulid=membership.ulid,
      user_ulid=membership.user_ulid,
      account_ulid=membership.account_ulid,
      role_ulid=membership.role_ulid,
      status=status_str,
      joined_at=membership.joined_at,
      removed_at=membership.removed_at
    )

  @staticmethod
  def orm_to_domain(membership_orm: MembershipORM) -> Membership:
    status_enum = MembershipStatus(membership_orm.status)
    return Membership(
      ulid=membership_orm.ulid,
      user_ulid=membership_orm.user_ulid,
      account_ulid=membership_orm.account_ulid,
      role_ulid=membership_orm.role_ulid,
      status=status_enum,
      joined_at=membership_orm.joined_at,
      removed_at=membership_orm.removed_at
    )
