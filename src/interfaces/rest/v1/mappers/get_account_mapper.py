from interfaces.rest.v1.dto.res.get_account_res import GetAccountRes
from services.models.outputs.get_account_som import GetAccountSOM


class GetAccountMapper:
  @staticmethod
  def som_to_res(get_account_som: GetAccountSOM) -> GetAccountRes:
    return GetAccountRes(
      uuid=get_account_som.uuid,
      name=get_account_som.name,
      age=get_account_som.age,
      account_type=get_account_som.account_type.value
    )
