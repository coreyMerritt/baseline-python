from typing import Protocol

from interfaces.rest.models.infrastructure_collection import InfrastructureCollection
from interfaces.rest.models.repository_collection import RepositoryCollection


class ProjectnameState(Protocol):
  infra: InfrastructureCollection
  repos: RepositoryCollection
