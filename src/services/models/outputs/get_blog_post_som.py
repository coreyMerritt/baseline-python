from dataclasses import dataclass


@dataclass
class GetBlogPostSOM:
  user_id: int
  id: int
  title: str
  body: str
