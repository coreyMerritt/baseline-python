from domain.entities.account import Account
from domain.exceptions.domain_mapper_exception import DomainMapperException
from domain.mappers.account_type_mapper import AccountTypeMapper
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq
from interfaces.rest.v1.dto.res.create_account_res import CreateAccountRes
from interfaces.rest.v1.exceptions.rest_adapter_exception import RestAdapterException


class CreateAccountAdapter:
  @staticmethod
  def req_to_domain(req: CreateAccountReq) -> Account:
    try:
      account_type = AccountTypeMapper.str_to_enum(req.account_type)
    except DomainMapperException as e:
      raise RestAdapterException(str(e)) from e
    return Account(
      name=req.name,
      age=req.age,
      account_type=account_type
    )

  @staticmethod
  def domain_to_res(account: Account, status: str) -> CreateAccountRes:
    return CreateAccountRes(
      uuid=account.get_uid(),
      status=status
    )
