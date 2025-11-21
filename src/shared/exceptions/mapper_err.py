from shared.exceptions.projectname_exception import ProjectnameException


class MapperErr(ProjectnameException):
  message: str

  def __init__(self, *args):
    message="Mapping error occurred"
    self.message = message
    super().__init__(message, *args)
