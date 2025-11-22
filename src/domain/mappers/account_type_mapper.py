from domain.enums.account_type import AccountType
from shared.exceptions.enum_conversion_err import EnumConversionErr


class AccountTypeMapper:
  @staticmethod
  def str_to_enum(string: str) -> AccountType:
    for enum in AccountType:
      if string.lower() == enum.value.lower():
        return enum
    raise EnumConversionErr(string)
