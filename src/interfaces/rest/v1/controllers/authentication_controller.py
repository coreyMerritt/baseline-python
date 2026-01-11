import asyncio

from fastapi import Request

from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.v1.dto.req.auth.create_token_req import CreateTokenReq
from interfaces.rest.v1.mappers.auth.create_token_mapper import CreateTokenMapper
from services.authentication_manager import AuthenticationManager


class AuthenticationController:
  async def create_token(
    self,
    req: Request,
    body: CreateTokenReq,
  ) -> FooProjectNameHTTPResponse:
    authentication_manager = AuthenticationManager(
      logger=req.app.state.resources.infra.logger,
      user_repository=req.app.state.resources.repos.user,
      user_credential_repository=req.app.state.resources.repos.user_credential,
      password_verifier=req.app.state.resources.infra.password_verifier,
      token_issuer=req.app.state.resources.infra.token_issuer
    )
    sim = CreateTokenMapper.req_to_sim(body)
    som = await asyncio.to_thread(authentication_manager.create_token, sim)
    res = CreateTokenMapper.som_to_res(som)
    return FooProjectNameHTTPResponse(
      data=res
    )
