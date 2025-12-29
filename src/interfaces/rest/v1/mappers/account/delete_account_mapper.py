from interfaces.rest.v1.dto.res.account.delete_account_res import DeleteAccountRes
from services.models.outputs.account.delete_account_som import DeleteAccountSOM


class DeleteAccountMapper:
  @staticmethod
  def som_to_res(som: DeleteAccountSOM) -> DeleteAccountRes:
    return DeleteAccountRes(
      ulid=som.ulid,
      name=som.name,
      status=som.status,
      created_at=som.created_at,
      suspended_at=som.suspended_at,
      deleted_at=som.deleted_at
    )
