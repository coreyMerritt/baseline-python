from typing import Any

import psutil
import yaml

from infrastructure.base_infrastructure import Infrastructure
from infrastructure.disk.exceptions.disk_read_err import DiskReadErr
from shared.models.configs.disk_config import DiskConfig
from shared.models.health_reports.disk_health_report import DiskHealthReport


class Disk(Infrastructure):
  _disk_config: DiskConfig

  def __init__(self, disk_config: DiskConfig):
    self._disk_config = disk_config

  def get_health_report(self) -> DiskHealthReport:
    maximum_healthy_disk_usage_percentage = self._disk_config.maximum_healthy_disk_usage_percentage
    disk_usage_percentage = self._get_disk_usage_percentage()
    healthy = disk_usage_percentage <= maximum_healthy_disk_usage_percentage
    return DiskHealthReport(
      healthy=healthy
    )

  def read_yaml(self, yaml_path: str) -> Any:
    try:
      with open(yaml_path, "r", encoding='utf-8') as yaml_file:
        some_data = yaml.safe_load(yaml_file)
        return some_data
    except Exception as e:
      raise DiskReadErr(
        filename=yaml_path
      ) from e

  def _get_disk_usage_percentage(self) -> float:
    return psutil.disk_usage("/").percent
