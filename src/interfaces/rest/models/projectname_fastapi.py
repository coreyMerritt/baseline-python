from fastapi import FastAPI

from interfaces.rest.models.infrastructure_collection import InfrastructureCollection
from interfaces.rest.models.repository_collection import RepositoryCollection


class ProjectnameFastAPI(FastAPI):
  raw_infra: dict
  infra: InfrastructureCollection
  repos: RepositoryCollection
