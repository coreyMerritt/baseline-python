from pydantic import BaseModel


class FooProjectNameHTTPData(BaseModel):
  model_config = {"extra": "allow"}
