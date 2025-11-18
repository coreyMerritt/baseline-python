import requests
from pydantic import ValidationError

from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.external_services.exceptions.requests_parse_err import RequestsParseErr
from infrastructure.external_services.exceptions.requests_status_err import RequestsStatusErr
from shared.blog_post import BlogPost
from shared.models.configs.external_services.external_services_global_config import ExternalServicesGlobalConfig
from shared.models.configs.external_services.typicode_config import TypicodeConfig
from shared.models.health_reports.typicode_health_report import TypicodeHealthReport


class Typicode(Infrastructure):
  _external_global_config: ExternalServicesGlobalConfig
  _typicode_config: TypicodeConfig

  def __init__(self, external_global_config: ExternalServicesGlobalConfig, typicode_config: TypicodeConfig):
    self._external_global_config = external_global_config
    self._typicode_config = typicode_config

  def get_health_report(self) -> TypicodeHealthReport:
    try:
      self.get_blog_post(1, 1)
      healthy = True
    except Exception:
      healthy = False
    return TypicodeHealthReport(
      healthy=healthy
    )

  def get_blog_post(self, user_id: int, post_number: int) -> BlogPost:
    _ = user_id   # This mock-service doesnt actually ask for user_id, but its thematic to ask for it in this fn
    response = requests.get(
      url=f"https://jsonplaceholder.typicode.com/posts/{post_number}",
      timeout=self._external_global_config.request_timeout
    )
    try:
      response.raise_for_status()
    except requests.exceptions.HTTPError as e:
      raise RequestsStatusErr(response.status_code, response.reason) from e
    try:
      response_json = response.json()
      blog_post = BlogPost.model_validate(response_json)
    except (ValueError, ValidationError, KeyError) as e:
      raise RequestsParseErr() from e
    return blog_post
