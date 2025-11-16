from pydantic import BaseModel


class ProjectnameHTTPError(BaseModel):
  message: str
