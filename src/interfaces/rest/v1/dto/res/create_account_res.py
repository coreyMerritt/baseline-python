from pydantic import BaseModel


class CreateAccountRes(BaseModel):
  uuid: str
  status: str
