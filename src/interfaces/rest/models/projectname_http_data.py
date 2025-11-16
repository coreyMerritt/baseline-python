from pydantic import BaseModel


class ProjectnameHTTPData(BaseModel):
  model_config = {"extra": "allow"}
