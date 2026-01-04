from fastapi import Request
from fastapi.datastructures import URL, Headers

from composition.models.infrastructure_collection import InfrastructureCollection
from composition.models.repository_collection import RepositoryCollection
from interfaces.rest.models.foo_project_name_fastapi import FooProjectNameFastAPI
from interfaces.rest.models.foo_project_name_state import FooProjectNameState


class FooProjectNameRequest:
  def __init__(self, req: Request):
    self._req = req

  @property
  def infra(self) -> InfrastructureCollection:
    state: FooProjectNameState = self._req.app.state
    return state.resources.infra

  @property
  def repos(self) -> RepositoryCollection:
    state: FooProjectNameState = self._req.app.state
    return state.resources.repos

  @property
  def app(self) -> FooProjectNameFastAPI:
    return self._req.app

  @property
  def client_ip(self) -> str:
    client = self._req.client
    client_ip = client.host if client else ""
    return str(client_ip)

  @property
  def correlation_id(self) -> str:
    return self._req.state.correlation_id

  @property
  def endpoint(self) -> str:
    return self._req.url.path

  @property
  def headers(self) -> Headers:
    return self._req.headers

  @property
  def method(self) -> str:
    return self._req.method

  @property
  def request_id(self) -> str:
    return self._req.state.request_id

  @property
  def route(self) -> str:
    route = self._req.scope.get("route")
    route_path = route.path if route else ""
    return route_path if route_path else ""

  @property
  def url(self) -> URL:
    return self._req.url

  @property
  def user_agent(self) -> str:
    user_agent = self._req.headers.get("user-agent")
    return user_agent if user_agent else ""


def get_foo_project_name_request(req: Request) -> FooProjectNameRequest:
  return FooProjectNameRequest(req)
