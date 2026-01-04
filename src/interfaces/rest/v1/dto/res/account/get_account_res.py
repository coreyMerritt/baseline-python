from datetime import datetime

from interfaces.rest.models.foo_project_name_http_data import FooProjectNameHTTPData


class GetAccountRes(FooProjectNameHTTPData):
  ulid: str
  name: str
  status: str
  created_at: datetime
  suspended_at: datetime | None
  deleted_at: datetime | None
