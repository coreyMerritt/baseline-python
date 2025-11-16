from domain.enums.account_type import AccountType
from domain.exceptions.mapper_err import MapperErr


class AccountTypeMapper:
  @staticmethod
  def str_to_enum(string: str) -> AccountType:
    for enum in AccountType:
      if string.lower() == enum.value.lower():
        return enum
    raise MapperErr()

  @staticmethod
  def enum_to_str(enum: AccountType) -> str:
    return enum.value
