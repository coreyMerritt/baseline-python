from domain.enums.account_status import AccountStatus
from domain.subdomain.entities.account import Account
from infrastructure.database.orm.account_orm import AccountORM


class AccountMapper:
  @staticmethod
  def domain_to_orm(account: Account) -> AccountORM:
    status_str = account.status.value
    return AccountORM(
      ulid=account.ulid,
      name=account.name,
      status=status_str,
      created_at=account.created_at,
      suspended_at=account.suspended_at,
      deleted_at=account.deleted_at
    )

  @staticmethod
  def orm_to_domain(account_orm: AccountORM) -> Account:
    status_enum = AccountStatus(account_orm.status)
    return Account(
      ulid=account_orm.ulid,
      name=account_orm.name,
      status=status_enum,
      created_at=account_orm.created_at,
      suspended_at=account_orm.suspended_at,
      deleted_at=account_orm.deleted_at
    )
