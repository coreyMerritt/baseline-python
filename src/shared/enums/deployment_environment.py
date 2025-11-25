from enum import Enum


class DeploymentEnvironment(str, Enum):
  DEV = "dev"
  PROD = "prod"
  TEST = "test"
