from interfaces.rest.models.projectname_http_data import ProjectnameHTTPData


class GetAccountRes(ProjectnameHTTPData):
  uuid: str
  name: str
  age: int
  account_type: str
