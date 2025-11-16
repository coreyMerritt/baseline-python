from domain.enums.account_type import AccountType
from domain.exceptions.domain_mapper_err import DomainMapperErr


class AccountTypeMapper:
  @staticmethod
  def str_to_enum(string: str) -> AccountType:
    for enum in AccountType:
      if string.lower() == enum.value.lower():
        return enum
    raise DomainMapperErr()

  @staticmethod
  def enum_to_str(enum: AccountType) -> str:
    return enum.value
