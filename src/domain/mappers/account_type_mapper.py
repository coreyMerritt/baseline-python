from domain.enums.account_type import AccountType
from domain.exceptions.domain_mapper_exception import DomainMapperException


class AccountTypeMapper:
  @staticmethod
  def str_to_enum(account_type: str) -> AccountType:
    if account_type.lower() == AccountType.BUSINESS.value.lower():
      return AccountType.BUSINESS
    if account_type.lower() == AccountType.PERSONAL.value.lower():
      return AccountType.PERSONAL
    raise DomainMapperException()

  @staticmethod
  def enum_to_str(account_type: AccountType) -> str:
    return account_type.value
