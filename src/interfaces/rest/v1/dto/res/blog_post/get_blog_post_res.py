from interfaces.rest.models.foo_project_name_http_data import FooProjectNameHTTPData


class GetBlogPostRes(FooProjectNameHTTPData):
  user_id: int
  id: int
  title: str
  body: str
