from domain.mappers.account_type_mapper import AccountTypeMapper
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq
from interfaces.rest.v1.dto.res.create_account_res import CreateAccountRes
from services.models.inputs.create_account_sim import CreateAccountSIM
from services.models.outputs.create_account_som import CreateAccountSOM


class CreateAccountMapper:
  @staticmethod
  def req_to_servicemodel(req: CreateAccountReq) -> CreateAccountSIM:
    account_type = AccountTypeMapper.str_to_enum(req.account_type)
    return CreateAccountSIM(
      uuid=None,
      name=req.name,
      age=req.age,
      account_type=account_type
    )

  @staticmethod
  def servicemodel_to_res(account_created_service_model: CreateAccountSOM, status: str) -> CreateAccountRes:
    return CreateAccountRes(
      uuid=account_created_service_model.uuid,
      status=status
    )
