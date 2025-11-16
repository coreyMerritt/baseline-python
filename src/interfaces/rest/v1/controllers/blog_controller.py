import asyncio
from logging import Logger

from fastapi import Request

from interfaces.rest.exceptions.projectname_http_exception import ProjectnameHTTPException
from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.v1.adapters.get_blog_adapter import GetBlogAdapter
from services.blog_manager import BlogManager
from services.exceptions.item_not_found_err import ItemNotFoundErr
from services.log_manager import LogManager


class BlogController:
  _req: Request
  _logger: Logger
  _blog_manager: BlogManager

  def __init__(self, req: Request):
    self._req = req
    self._logger = LogManager.get_logger(self.__class__.__name__)
    self._blog_manager = BlogManager()

  async def get_blog_post(self, user_id: int, post_number: int) -> ProjectnameHTTPResponse:
    try:
      blog_post = await asyncio.to_thread(
        self._blog_manager.get_blog_post,
        user_id,
        post_number
      )
      if not blog_post:
        self._logger.warning("No existing blog found for user_id-post_number: %s-%s", user_id, post_number)
        raise ProjectnameHTTPException(
          status_code=404,
          message="Blog not found"
        )
      self._logger.info("Successfully retrieved blog for user_id-post_number: %s-%s", user_id, post_number)
      get_blog_res = GetBlogAdapter.external_to_res(blog_post)
      return ProjectnameHTTPResponse(
        data=get_blog_res
      )
    except ItemNotFoundErr as e:
      self._logger.error(
        "Failed to get blog for user_id-post_number: %s-%s",
        user_id,
        post_number,
        exc_info=e
      )
      raise ProjectnameHTTPException(
        status_code=404,
        message="Blog not found"
      ) from e
    except RestAdapterErr as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      # We give proper error codes when possible with "detail" matching the error code summary
      raise ProjectnameHTTPException(
        status_code=400,
        message="Bad request"
      ) from e
