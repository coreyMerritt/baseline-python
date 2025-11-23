from fastapi import FastAPI

from interfaces.rest.types.infrastructure_collection import InfrastructureCollection
from interfaces.rest.types.repository_collection import RepositoryCollection


class ProjectnameFastAPI(FastAPI):
  infra: InfrastructureCollection
  repos: RepositoryCollection
