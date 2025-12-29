from pydantic import BaseModel


class CreateUserReq(BaseModel):
  username: str
  email_address: str
