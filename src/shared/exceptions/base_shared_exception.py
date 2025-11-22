from shared.enums.exception_type import ExceptionType
from shared.exceptions.projectname_exception import ProjectnameException


class BaseSharedException(ProjectnameException):
  exception_type = ExceptionType.SHARED
