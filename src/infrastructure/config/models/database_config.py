from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
  engine: str
  username: str
  password: str
  host: str
  port: int
  name: str
