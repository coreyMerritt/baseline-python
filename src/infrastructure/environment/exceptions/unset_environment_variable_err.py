from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class UnsetEnvironmentVariableErr(InfrastructureException):
  message: str

  def __init__(self, env_var_name: str, *args):
    message=f"Environment variable not set: {env_var_name}"
    self.message = message
    super().__init__(message, *args)
