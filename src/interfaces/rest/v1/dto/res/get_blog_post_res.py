from pydantic import BaseModel


class GetBlogPostRes(BaseModel):
  user_id: int
  id: int
  title: str
  body: str
