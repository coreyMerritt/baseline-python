from interfaces.rest.v1.dto.res.account.get_account_res import GetAccountRes
from services.models.outputs.account.get_account_som import GetAccountSOM


class GetAccountMapper:
  @staticmethod
  def som_to_res(som: GetAccountSOM) -> GetAccountRes:
    return GetAccountRes(
      ulid=som.ulid,
      name=som.name,
      status=som.status,
      created_at=som.created_at,
      suspended_at=som.suspended_at,
      deleted_at=som.deleted_at
    )
