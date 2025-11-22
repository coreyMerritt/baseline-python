from domain.entities.account import Account
from domain.mappers.account_type_mapper import AccountTypeMapper
from infrastructure.database.orm.account_orm import AccountORM


class AccountMapper:
  @staticmethod
  def domain_to_orm(account: Account) -> AccountORM:
    return AccountORM(
      uuid=account.uuid,
      name=account.name,
      age=account.age,
      account_type=account.account_type.value
    )

  @staticmethod
  def orm_to_domain(account_orm: AccountORM) -> Account:
    account_type = AccountTypeMapper.str_to_enum(account_orm.account_type)
    return Account(
      uuid=account_orm.uuid,
      name=account_orm.name,
      age=account_orm.age,
      account_type=account_type
    )
