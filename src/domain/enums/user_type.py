from enum import Enum


class UserType(str, Enum):
  ADMIN = "admin"
  READ_ONLY_CLIENT = "read-only client"
  STANDARD = "standard"
