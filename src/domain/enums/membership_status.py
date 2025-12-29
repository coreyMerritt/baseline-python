from enum import Enum


class MembershipStatus(str, Enum):
  ACTIVE = "active"
  INVITED = "invited"
  REMOVED = "removed"
