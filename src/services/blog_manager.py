from infrastructure.config.config_manager import ConfigManager
from infrastructure.external_services.exceptions.requests_parse_exception import RequestsParseException
from infrastructure.external_services.exceptions.requests_status_exception import RequestsStatusException
from infrastructure.external_services.typicode.typicode_manager import TypicodeManager
from services.abc_service import Service
from services.exceptions.blog_retrieval_exception import BlogRetrievalException


class BlogManager(Service):
  _typicode_manager: TypicodeManager

  def __init__(self):
    external_config = ConfigManager.get_external_config()
    self._typicode_manager = TypicodeManager(external_config.global_, external_config.typicode)
    super().__init__()

  def get_blog_post(self, user_id: int, post_number: int):
    try:
      return self._typicode_manager.get_blog_post(user_id, post_number)
    except RequestsParseException as e:
      raise BlogRetrievalException(str(e)) from e
    except RequestsStatusException as e:
      raise BlogRetrievalException(str(e)) from e
