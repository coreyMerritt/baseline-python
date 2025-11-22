from dataclasses import dataclass

from infrastructure.database.account_repository import AccountRepository
from infrastructure.external_services.blog_post_repository import BlogPostRepository


@dataclass
class Repo:
  account: AccountRepository
  blog_post: BlogPostRepository
