from typing import Any

import yaml

from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.disk.exceptions.disk_read_err import DiskReadErr


class Disk(Infrastructure):
  def read_yaml(self, yaml_path: str) -> Any:
    try:
      with open(yaml_path, "r", encoding='utf-8') as yaml_file:
        some_data = yaml.safe_load(yaml_file)
        return some_data
    except Exception as e:
      raise DiskReadErr(
        filename=yaml_path
      ) from e
