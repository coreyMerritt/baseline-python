from domain.interfaces.repositories.blog_post_repository_interface import BlogPostRepositoryInterface
from infrastructure.types.logger_interface import LoggerInterface
from services.base_service import BaseService
from services.mappers.get_blog_post_mapper import GetBlogPostMapper
from services.models.outputs.get_blog_post_som import GetBlogPostSOM


class BlogManager(BaseService):
  _blog_post_repository: BlogPostRepositoryInterface

  def __init__(
    self,
    logger: LoggerInterface,
    blog_post_repository: BlogPostRepositoryInterface
  ):
    self._blog_post_repository = blog_post_repository
    super().__init__(logger)

  def get_blog_post(self, user_id: int, post_number: int) -> GetBlogPostSOM:
    try:
      blog_post = self._blog_post_repository.get(user_id, post_number)
    except Exception as e:
      self._raise_service_exception(e)
    blog_post_som = GetBlogPostMapper.blog_post_to_som(blog_post)
    return blog_post_som
