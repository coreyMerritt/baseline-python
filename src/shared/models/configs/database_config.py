from dataclasses import dataclass

from shared.models.configs.base_config import Config


@dataclass(frozen=True)
class DatabaseConfig(Config):
  engine: str
  host: str
  name: str
  password: str
  port: int
  username: str
