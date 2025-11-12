from pydantic import BaseModel, ConfigDict, Field


class BlogPost(BaseModel):
  user_id: int = Field(alias="userId")
  id: int
  title: str
  body: str

  model_config = ConfigDict(populate_by_name=True)
