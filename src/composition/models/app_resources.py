from dataclasses import dataclass

from composition.models.infrastructure_collection import InfrastructureCollection
from composition.models.repository_collection import RepositoryCollection


@dataclass
class AppResources:
  infra: InfrastructureCollection
  repos: RepositoryCollection
