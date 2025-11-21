from typing import Protocol

from domain.entities.blog_post import BlogPost


class BlogPostRepositoryInterface(Protocol):
  def get(self, user_id: int, post_number: int) -> BlogPost: ...
