from dataclasses import dataclass


@dataclass
class HealthReport():
  healthy: bool

  def __post_init__(self):
    assert not isinstance(self, HealthReport), "HealthReport is a base class and should not be instantiated"
