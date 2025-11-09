from domain.enums.account_type import AccountType
from domain.exceptions.domain_mapper_exception import DomainMapperException


class AccountTypeMapper:
  @staticmethod
  def str_to_enum(string: str) -> AccountType:
    for enum in AccountType:
      if string.lower() == enum.value.lower():
        return enum
    raise DomainMapperException()

  @staticmethod
  def enum_to_str(enum: AccountType) -> str:
    return enum.value
