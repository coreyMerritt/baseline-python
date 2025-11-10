from abc import ABC, abstractmethod

from infrastructure.models.abc_health_report import HealthReport


class Infrastructure(ABC):
  @abstractmethod
  def get_health_report(self, *args, **kwargs) -> HealthReport:
    pass
