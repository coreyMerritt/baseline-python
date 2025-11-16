from infrastructure.external_services.exceptions.requests_parse_err import RequestsParseErr
from infrastructure.external_services.exceptions.requests_status_err import RequestsStatusErr
from infrastructure.external_services.typicode.typicode_manager import TypicodeManager
from services.abc_service import Service
from services.config_manager import ConfigManager
from services.exceptions.item_not_found_err import ItemNotFoundErr


class BlogManager(Service):
  _typicode_manager: TypicodeManager

  def __init__(self):
    external_config = ConfigManager.get_external_config()
    self._typicode_manager = TypicodeManager(external_config.global_, external_config.typicode)
    super().__init__()

  def get_blog_post(self, user_id: int, post_number: int):
    try:
      return self._typicode_manager.get_blog_post(user_id, post_number)
    except RequestsParseErr as e:
      raise ItemNotFoundErr(str(e)) from e
    except RequestsStatusErr as e:
      raise ItemNotFoundErr(str(e)) from e
