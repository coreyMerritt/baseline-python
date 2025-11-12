from enum import Enum


class EnvironmentType(str, Enum):
  DEV = "dev"
  PROD = "prod"
  TEST = "test"
