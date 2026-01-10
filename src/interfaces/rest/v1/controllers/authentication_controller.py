from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest
from interfaces.rest.v1.dto.req.auth.create_token_req import CreateTokenReq
from interfaces.rest.v1.mappers.auth.create_token_mapper import CreateTokenMapper
from services.authentication_manager import AuthenticationManager


class AuthenticationController:
  async def create_token(
    self,
    req: FooProjectNameRequest,
    body: CreateTokenReq,
  ) -> FooProjectNameHTTPResponse:
    authentication_manager = AuthenticationManager(
      logger=req.infra.logger,
      membership_repository=req.repos.membership,
      user_repository=req.repos.user,
      user_credential_repository=req.repos.user_credential,
      password_verifier=req.infra.password_verifier,
      token_issuer=req.infra.token_issuer
    )
    sim = CreateTokenMapper.req_to_sim(body)
    som = authentication_manager.create_token(sim)
    res = CreateTokenMapper.som_to_res(som)
    return FooProjectNameHTTPResponse(
      data=res
    )
