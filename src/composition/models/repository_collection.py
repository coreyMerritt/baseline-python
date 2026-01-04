from dataclasses import dataclass

from infrastructure.database.repositories.account_repository import AccountRepository
from infrastructure.database.repositories.membership_repository import MembershipRepository
from infrastructure.database.repositories.role_repository import RoleRepository
from infrastructure.database.repositories.user_repository import UserRepository
from infrastructure.external_services.blog_post_repository import BlogPostRepository


@dataclass
class RepositoryCollection:
  account: AccountRepository
  blog_post: BlogPostRepository
  membership: MembershipRepository
  role: RoleRepository
  user: UserRepository
