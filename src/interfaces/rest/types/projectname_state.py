from typing import Protocol

from interfaces.rest.types.infrastructure_collection import InfrastructureCollection
from interfaces.rest.types.repository_collection import RepositoryCollection


class ProjectnameState(Protocol):
  infra: InfrastructureCollection
  repos: RepositoryCollection
