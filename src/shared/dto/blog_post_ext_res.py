from pydantic import BaseModel, ConfigDict, Field


# NOTE: This should really be in infra/external/typicode, however we're cutting some corners on getting this
#       to the API easier as this only exists to show an example of using an External service/API
class BlogPostExtRes(BaseModel):
  user_id: int = Field(alias="userId")
  id: int
  title: str
  body: str

  model_config = ConfigDict(populate_by_name=True)
