from enum import Enum


class AccountStatus(str, Enum):
  ACTIVE = "active"
  SUSPENDED = "suspended"
  DELETED = "deleted"
