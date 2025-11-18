# TOsDO: Doesnt inherit from infra err, leaving this as a test for a new linting script
class UnsetEnvironmentVariableErr(Exception):
  message: str

  def __init__(self, env_var_name: str, *args):
    message=f"Environment variable not set: {env_var_name}"
    self.message = message
    super().__init__(message, *args)
