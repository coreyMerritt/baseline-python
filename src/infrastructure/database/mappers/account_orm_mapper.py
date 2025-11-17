from domain.entities.account import Account
from domain.exceptions.domain_mapper_err import DomainMapperErr
from domain.mappers.account_type_mapper import AccountTypeMapper
from infrastructure.database.exceptions.database_mapper_err import DatabaseMapperErr
from infrastructure.database.orm.account_orm import AccountORM


class AccountMapper:
  @staticmethod
  def domain_to_orm(account: Account) -> AccountORM:
    try:
      account_type = AccountTypeMapper.enum_to_str(account.get_account_type())
    except DomainMapperErr as e:
      raise DomainMapperErr() from e
    return AccountORM(
      uuid=account.get_uuid(),
      name=account.get_name(),
      age=account.get_age(),
      account_type=account_type
    )

  @staticmethod
  def orm_to_domain(account_orm: AccountORM) -> Account:
    assert isinstance(account_orm.name, str)
    assert isinstance(account_orm.age, int)
    assert isinstance(account_orm.account_type, str)
    try:
      account_type = AccountTypeMapper.str_to_enum(account_orm.account_type)
    except DomainMapperErr as e:
      raise DatabaseMapperErr() from e
    return Account(
      uuid=account_orm.uuid,
      name=account_orm.name,
      age=account_orm.age,
      account_type=account_type
    )
