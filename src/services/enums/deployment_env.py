from enum import Enum


class DeploymentEnv(str, Enum):
  DEV = "dev"
  PROD = "prod"
  TEST = "test"
