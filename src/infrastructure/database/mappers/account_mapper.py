from domain.entities.account import Account
from infrastructure.database.orm.account_orm import AccountORM
from shared.mappers.account_type_mapper import AccountTypeMapper


class AccountMapper:
  @staticmethod
  def domain_to_orm(account: Account) -> AccountORM:
    account_type = AccountTypeMapper.enum_to_str(account.account_type)
    return AccountORM(
      uuid=account.uuid,
      name=account.name,
      age=account.age,
      account_type=account_type
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
