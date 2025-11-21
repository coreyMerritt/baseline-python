from interfaces.rest.v1.dto.res.get_account_res import GetAccountRes
from services.models.outputs.get_account_som import GetAccountSOM
from shared.mappers.account_type_mapper import AccountTypeMapper


class GetAccountMapper:
  @staticmethod
  def som_to_res(get_account_som: GetAccountSOM) -> GetAccountRes:
    account_type = AccountTypeMapper.enum_to_str(get_account_som.account_type)
    return GetAccountRes(
      uuid=get_account_som.uuid,
      name=get_account_som.name,
      age=get_account_som.age,
      account_type=account_type
    )
