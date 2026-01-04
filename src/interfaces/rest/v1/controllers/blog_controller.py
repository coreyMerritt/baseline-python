import asyncio

from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest
from interfaces.rest.v1.mappers.blog_post.get_blog_post_mapper import GetBlogPostMapper
from services.blog_manager import BlogManager


class BlogController:
  async def get_blog_post(self, req: FooProjectNameRequest, user_id: int, post_number: int) -> FooProjectNameHTTPResponse:
    blog_manager = BlogManager(
      req.infra.logger,
      req.repos.blog_post
    )
    blog_post_som = await asyncio.to_thread(
      blog_manager.get_blog_post,
      user_id,
      post_number
    )
    get_blog_res = GetBlogPostMapper.som_to_res(blog_post_som)
    return FooProjectNameHTTPResponse(
      data=get_blog_res
    )
