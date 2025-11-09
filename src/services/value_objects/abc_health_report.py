from abc import ABC
from dataclasses import dataclass


@dataclass
class HealthReport(ABC):
  healthy: bool
