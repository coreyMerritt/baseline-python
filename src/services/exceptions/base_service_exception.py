from shared.enums.exception_type import ExceptionType
from shared.exceptions.foo_project_name_exception import FooProjectNameException


class BaseServiceException(FooProjectNameException):
  exception_type = ExceptionType.SERVICE
