from typing import Generic, TypeVar

from pydantic import BaseModel

from interfaces.rest.models.foo_project_name_http_error import FooProjectNameHTTPError

T = TypeVar("T", bound=BaseModel)

class FooProjectNameHTTPResponse(BaseModel, Generic[T]):
  data: T | None = None
  error: FooProjectNameHTTPError | None = None
