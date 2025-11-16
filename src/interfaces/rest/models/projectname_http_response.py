from typing import Generic, TypeVar

from pydantic import BaseModel

from interfaces.rest.models.projectname_http_error import ProjectnameHTTPError

T = TypeVar("T", bound=BaseModel)

class ProjectnameHTTPResponse(BaseModel, Generic[T]):
  data: T | None = None
  error: ProjectnameHTTPError | None = None
