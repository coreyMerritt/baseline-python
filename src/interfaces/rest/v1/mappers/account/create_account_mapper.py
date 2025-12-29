from interfaces.rest.v1.dto.req.account.create_account_req import CreateAccountReq
from interfaces.rest.v1.dto.res.account.create_account_res import CreateAccountRes
from services.models.inputs.account.create_account_sim import CreateAccountSIM
from services.models.outputs.account.create_account_som import CreateAccountSOM


class CreateAccountMapper:
  @staticmethod
  def req_to_sim(req: CreateAccountReq) -> CreateAccountSIM:
    return CreateAccountSIM(
      name=req.name
    )

  @staticmethod
  def som_to_res(som: CreateAccountSOM) -> CreateAccountRes:
    return CreateAccountRes(
      ulid=som.ulid,
      name=som.name,
      status=som.status.value,
      created_at=som.created_at,
      suspended_at=som.suspended_at,
      deleted_at=som.deleted_at
    )
