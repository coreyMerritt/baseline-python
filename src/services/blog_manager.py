from infrastructure.external_services.exceptions.requests_parse_err import RequestsParseErr
from infrastructure.external_services.exceptions.requests_status_err import RequestsStatusErr
from infrastructure.external_services.typicode.typicode import Typicode
from infrastructure.logger.projectname_logger import ProjectnameLogger
from services.base_service import Service
from services.exceptions.item_not_found_err import ItemNotFoundErr
from shared.models.configs.external_services_config import ExternalServicesConfig
from shared.models.configs.typicode_config import TypicodeConfig


class BlogManager(Service):
  _typicode_manager: Typicode

  def __init__(
    self,
    logger: ProjectnameLogger,
    external_services_config: ExternalServicesConfig,
    typicode_config: TypicodeConfig
  ):
    self._typicode_manager = Typicode(
      external_services_config=external_services_config,
      typicode_config=typicode_config
    )
    super().__init__(logger)

  def get_blog_post(self, user_id: int, post_number: int):
    try:
      return self._typicode_manager.get_blog_post(user_id, post_number)
    except RequestsParseErr as e:
      raise ItemNotFoundErr() from e
    except RequestsStatusErr as e:
      raise ItemNotFoundErr() from e
