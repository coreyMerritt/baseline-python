from fastapi import FastAPI

from interfaces.rest.models.infrastructure_collection import InfrastructureCollection
from interfaces.rest.models.repository_collection import RepositoryCollection


class ProjectnameFastAPI(FastAPI):
  infra: InfrastructureCollection
  repos: RepositoryCollection
