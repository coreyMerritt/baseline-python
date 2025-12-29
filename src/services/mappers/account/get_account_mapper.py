from domain.subdomain.entities.account import Account
from services.models.outputs.account.get_account_som import GetAccountSOM


class GetAccountMapper:
  @staticmethod
  def entity_to_som(entity: Account) -> GetAccountSOM:
    return GetAccountSOM(
      ulid=entity.ulid,
      name=entity.name,
      status=entity.status,
      created_at=entity.created_at,
      suspended_at=entity.suspended_at,
      deleted_at=entity.deleted_at
    )
