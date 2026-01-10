from dataclasses import dataclass


@dataclass(frozen=True)
class GetBlogPostSOM:
  user_id: int
  id: int
  title: str
  body: str
