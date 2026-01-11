from interfaces.rest.models.foo_project_name_http_data import FooProjectNameHTTPData


class GetUserRes(FooProjectNameHTTPData):
  ulid: str
  username: str
  email_address: str
  user_type: str
