from abc import ABC, abstractmethod

from shared.models.health_reports.abc_health_report import HealthReport


class Infrastructure(ABC):
  @abstractmethod
  def get_health_report(self) -> HealthReport: ...
