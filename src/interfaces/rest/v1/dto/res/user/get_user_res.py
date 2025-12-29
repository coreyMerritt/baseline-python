from interfaces.rest.models.projectname_http_data import ProjectnameHTTPData


class GetUserRes(ProjectnameHTTPData):
  ulid: str
  username: str
  email_address: str
