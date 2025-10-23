from enum import Enum


class AccountType(str, Enum):
  BUSINESS = "business"
  PERSONAL = "personal"
