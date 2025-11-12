from enum import Enum


class ServerEnv(str, Enum):
  DEV = "dev"
  PROD = "prod"
  TEST = "test"
