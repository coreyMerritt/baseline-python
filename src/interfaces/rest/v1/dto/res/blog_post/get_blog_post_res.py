from interfaces.rest.models.projectname_http_data import ProjectnameHTTPData


class GetBlogPostRes(ProjectnameHTTPData):
  user_id: int
  id: int
  title: str
  body: str
