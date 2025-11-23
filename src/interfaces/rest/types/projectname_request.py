from fastapi import Request
from fastapi.datastructures import URL, Headers

from interfaces.rest.types.infrastructure_collection import InfrastructureCollection
from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.types.projectname_state import ProjectnameState
from interfaces.rest.types.repository_collection import RepositoryCollection


class ProjectnameRequest:
  def __init__(self, req: Request):
    self._req = req

  @property
  def infra(self) -> InfrastructureCollection:
    state: ProjectnameState = self._req.app.state
    return state.infra

  @property
  def repos(self) -> RepositoryCollection:
    state: ProjectnameState = self._req.app.state
    return state.repos

  @property
  def app(self) -> ProjectnameFastAPI:
    return self._req.app

  @property
  def headers(self) -> Headers:
    return self._req.headers

  @property
  def method(self) -> str:
    return self._req.method

  @property
  def url(self) -> URL:
    return self._req.url


def get_projectname_request(req: Request) -> ProjectnameRequest:
  return ProjectnameRequest(req)
