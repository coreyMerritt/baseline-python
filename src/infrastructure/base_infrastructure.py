from abc import ABC, abstractmethod

from shared.models.health_reports.base_health_report import HealthReport


class BaseInfrastructure(ABC):
  def __init__(self):
    assert type(self) is not BaseInfrastructure, "BaseInfrastructure is a base class and should not be instantiated"

  @abstractmethod
  def get_health_report(self) -> HealthReport: ...
