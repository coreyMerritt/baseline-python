import requests
from pydantic import ValidationError

from infrastructure.config.models.external_config import ExternalConfig
from infrastructure.external.exceptions.requests_parse_exception import RequestsParseException
from infrastructure.external.exceptions.requests_status_exception import RequestsStatusException
from infrastructure.external.typicode.models.blog_post import BlogPost


class TypicodeManager():
  _external_config: ExternalConfig

  def __init__(self, external_config: ExternalConfig):
    self._external_config = external_config

  def get_blog_post(self, user_id: int, post_number: int) -> BlogPost:
    _ = user_id   # This mock-service doesnt actually ask for user_id, but its thematic to ask for it in this fn
    response = requests.get(
      url=f"https://jsonplaceholder.typicode.com/posts/{post_number}",
      timeout=self._external_config.request_timeout
    )
    try:
      response.raise_for_status()
    except requests.exceptions.HTTPError as e:
      raise RequestsStatusException(response.status_code, response.reason) from e
    try:
      response_json = response.json()
      blog_post = BlogPost.model_validate(response_json)
    except (ValueError, ValidationError, KeyError) as e:
      raise RequestsParseException() from e
    return blog_post
