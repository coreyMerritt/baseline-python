import requests
from pydantic import ValidationError

from infrastructure.base_infrastructure import BaseInfrastructure
from infrastructure.external_services.dto.res.blog_post_ext_res import BlogPostExtRes
from infrastructure.external_services.exceptions.requests_parse_err import RequestsParseErr
from infrastructure.external_services.exceptions.requests_status_err import RequestsStatusErr
from infrastructure.external_services.models.external_services_config import ExternalServicesConfig
from infrastructure.external_services.models.typicode_config import TypicodeConfig
from infrastructure.external_services.models.typicode_health_report import TypicodeHealthReport


class TypicodeClient(BaseInfrastructure):
  _request_timeout: float
  _placeholder: str

  def __init__(self, external_services_config: ExternalServicesConfig, typicode_config: TypicodeConfig):
    self._request_timeout = external_services_config.request_timeout
    self._placeholder = typicode_config.placeholder
    super().__init__()

  def get_health_report(self) -> TypicodeHealthReport:
    try:
      self.get_blog_post_ext_res(1, 1)
      healthy = True
    except Exception:
      healthy = False
    return TypicodeHealthReport(
      healthy=healthy
    )

  def get_blog_post_ext_res(self, user_id: int, post_number: int) -> BlogPostExtRes:
    _ = user_id   # This mock-service doesnt actually ask for user_id, but its thematic to ask for it in this fn
    response = requests.get(
      url=f"https://jsonplaceholder.typicode.com/posts/{post_number}",
      timeout=self._request_timeout
    )
    try:
      response.raise_for_status()
    except requests.exceptions.HTTPError as e:
      raise RequestsStatusErr(response.status_code, response.reason) from e
    try:
      response_json = response.json()
      blog_post_ext_res = BlogPostExtRes.model_validate(response_json)
    except (ValueError, ValidationError, KeyError) as e:
      raise RequestsParseErr() from e
    return blog_post_ext_res
