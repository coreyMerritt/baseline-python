from fastapi import APIRouter, Depends

from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest, get_foo_project_name_request
from interfaces.rest.v1.controllers.blog_controller import BlogController

controller = BlogController()
router = APIRouter(prefix="/api/v1/blog")

# This example is basically just a full passthrough to an external service, 0 transformation
@router.get(
  path="",
  response_model=FooProjectNameHTTPResponse,
  status_code=200
)
async def get_blog(
  user_id: int,
  post_number: int,
  req: FooProjectNameRequest = Depends(get_foo_project_name_request)
) -> FooProjectNameHTTPResponse:
  return await controller.get_blog_post(
    req=req,
    user_id=user_id,
    post_number=post_number
  )
