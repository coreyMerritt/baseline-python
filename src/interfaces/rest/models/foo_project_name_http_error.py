from pydantic import BaseModel


class FooProjectNameHTTPError(BaseModel):
  message: str
