from datetime import datetime

from interfaces.rest.models.projectname_http_data import ProjectnameHTTPData


class UpdateAccountRes(ProjectnameHTTPData):
  ulid: str
  name: str
  status: str
  created_at: datetime
  suspended_at: datetime | None
  deleted_at: datetime | None
