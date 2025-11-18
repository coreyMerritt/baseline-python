from abc import ABC, abstractmethod

from shared.models.health_reports.base_health_report import HealthReport


class Infrastructure(ABC):
  def __init__(self):
    assert not isinstance(self, Infrastructure), "Infrastructure is a base class and should not be instantiated"

  @abstractmethod
  def get_health_report(self) -> HealthReport: ...
