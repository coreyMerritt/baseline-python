import asyncio
from logging import Logger

from fastapi import HTTPException, Request

from infrastructure.logging.log_manager import LogManager
from interfaces.rest.v1.adapters.get_blog_adapter import GetBlogAdapter
from interfaces.rest.v1.dto.res.get_blog_post_res import GetBlogPostRes
from interfaces.rest.v1.exceptions.rest_adapter_exception import RestAdapterException
from services.blog_manager import BlogManager
from services.exceptions.blog_retrieval_exception import BlogRetrievalException


class BlogController:
  _req: Request
  _logger: Logger
  _blog_manager: BlogManager

  def __init__(self, req: Request):
    self._req = req
    self._logger = LogManager.get_logger(self.__class__.__name__)
    self._blog_manager = BlogManager()

  async def get_blog_post(self, user_id: int, post_number: int) -> GetBlogPostRes:
    try:
      blog_post = await asyncio.to_thread(
        self._blog_manager.get_blog_post,
        user_id,
        post_number
      )
      if not blog_post:
        self._logger.warning("No existing blog found for user_id-post_number: %s-%s", user_id, post_number)
        raise HTTPException(status_code=404, detail="Blog not found")
      self._logger.info("Successfully retrieved blog for user_id-post_number: %s-%s", user_id, post_number)
      return GetBlogAdapter.external_to_res(blog_post)
    except BlogRetrievalException as e:
      self._logger.error(
        "Failed to get blog for user_id-post_number: %s-%s",
        user_id,
        post_number,
        exc_info=e
      )
      raise HTTPException(status_code=500, detail="Internal server error") from e
    except RestAdapterException as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      # We give proper error codes when possible with "detail" matching the error code summary
      raise HTTPException(status_code=400, detail="Bad request") from e
