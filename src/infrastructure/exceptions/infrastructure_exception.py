from shared.enums.exception_type import ExceptionType
from shared.exceptions.projectname_exception import ProjectnameException


class BaseInfrastructureException(ProjectnameException):
  exception_type = ExceptionType.INFRASTRUCTURE
