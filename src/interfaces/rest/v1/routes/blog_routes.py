from fastapi import APIRouter

from infrastructure.logging.log_manager import LogManager
from interfaces.rest.v1.controllers.blog_controller import BlogController
from interfaces.rest.v1.dto.res.get_blog_post_res import GetBlogPostRes

router = APIRouter(prefix="/api/v1/blog")

# This example is basically just a full passthrough to an external service, 0 transformation
@router.get(
  path="/",
  response_model=GetBlogPostRes,
  status_code=200
)
async def get_blog(user_id: int, post_number: int) -> GetBlogPostRes:
  controller = BlogController()
  return await controller.get_blog_post(user_id=user_id, post_number=post_number)
