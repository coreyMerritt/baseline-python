from dataclasses import dataclass

from domain.enums.membership_status import MembershipStatus


@dataclass
class CreateMembershipSIM:
  user_ulid: str
  account_ulid: str
  role_ulid: str
  status: MembershipStatus
