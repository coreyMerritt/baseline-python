from domain.entities.blog_post import BlogPost
from domain.exceptions.repository_data_integrity_err import RepositoryDataIntegrityErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.blog_post_repository_interface import BlogPostRepositoryInterface
from infrastructure.external_services.exceptions.requests_parse_err import RequestsParseErr
from infrastructure.external_services.exceptions.requests_status_err import RequestsStatusErr
from infrastructure.external_services.mappers.blog_post_mapper import BlogPostMapper
from infrastructure.external_services.typicode_client import TypicodeClient
from shared.exceptions.mapper_err import MapperErr
from shared.models.configs.external_services_config import ExternalServicesConfig
from shared.models.configs.typicode_config import TypicodeConfig


class BlogPostRepository(BlogPostRepositoryInterface):
  _typicode_client: TypicodeClient

  def __init__(self, external_services_config: ExternalServicesConfig, typicode_config: TypicodeConfig):
    self._typicode_client = TypicodeClient(
      external_services_config,
      typicode_config
    )

  def get(self, user_id: int, post_number: int) -> BlogPost:
    try:
      blog_post_ext_res = self._typicode_client.get_blog_post_ext_res(user_id, post_number)
    except RequestsStatusErr as e:
      raise RepositoryUnavailableErr() from e
    except RequestsParseErr as e:
      raise RepositoryDataIntegrityErr() from e
    try:
      blog_post = BlogPostMapper.ext_res_to_domain(blog_post_ext_res)
    except MapperErr as e:
      raise RepositoryDataIntegrityErr() from e
    return blog_post
