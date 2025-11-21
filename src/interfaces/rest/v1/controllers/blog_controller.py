import asyncio

from fastapi import Request

from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.v1.mappers.get_blog_post_mapper import GetBlogPostMapper
from services.blog_manager import BlogManager
from shared.types.logger_interface import LoggerInterface


class BlogController:
  _req: Request
  _logger: LoggerInterface
  _blog_manager: BlogManager

  def __init__(self, req: Request):
    self._req = req
    self._logger = req.app.state.logger
    self._blog_manager = BlogManager(
      req.app.state.logger,
      req.app.state.repository.blog_post
    )

  async def get_blog_post(self, user_id: int, post_number: int) -> ProjectnameHTTPResponse:
    blog_post_som = await asyncio.to_thread(
      self._blog_manager.get_blog_post,
      user_id,
      post_number
    )
    get_blog_res = GetBlogPostMapper.som_to_res(blog_post_som)
    return ProjectnameHTTPResponse(
      data=get_blog_res
    )
