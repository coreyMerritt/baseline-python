from domain.entities.account import Account
from domain.exceptions.domain_mapper_err import DomainMapperErr
from domain.mappers.account_type_mapper import AccountTypeMapper
from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.v1.dto.res.get_account_res import GetAccountRes


class GetAccountAdapter:
  @staticmethod
  def domain_to_res(account: Account) -> GetAccountRes:
    try:
      account_type = AccountTypeMapper.enum_to_str(account.get_account_type())
    except DomainMapperErr as e:
      raise RestAdapterErr(str(e)) from e
    return GetAccountRes(
      uuid=account.get_uuid(),
      name=account.get_name(),
      age=account.get_age(),
      account_type=account_type
    )
