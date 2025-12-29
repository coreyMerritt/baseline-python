from domain.enums.account_status import AccountStatus
from interfaces.rest.v1.dto.req.account.update_account_req import UpdateAccountReq
from interfaces.rest.v1.dto.res.account.update_account_res import UpdateAccountRes
from services.models.inputs.account.update_account_sim import UpdateAccountSIM
from services.models.outputs.account.update_account_som import UpdateAccountSOM


class UpdateAccountMapper:
  @staticmethod
  def req_to_sim(req: UpdateAccountReq) -> UpdateAccountSIM:
    return UpdateAccountSIM(
      ulid=req.ulid,
      name=req.name,
      status=AccountStatus(req.status)
    )

  @staticmethod
  def som_to_res(som: UpdateAccountSOM) -> UpdateAccountRes:
    return UpdateAccountRes(
      ulid=som.ulid,
      name=som.name,
      status=som.status.value,
      created_at=som.created_at,
      suspended_at=som.suspended_at,
      deleted_at=som.deleted_at
    )
