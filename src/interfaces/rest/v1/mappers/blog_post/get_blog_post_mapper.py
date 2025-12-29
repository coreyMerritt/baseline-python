from interfaces.rest.v1.dto.res.blog_post.get_blog_post_res import GetBlogPostRes
from services.models.outputs.get_blog_post_som import GetBlogPostSOM


class GetBlogPostMapper:
  @staticmethod
  def som_to_res(blog_post_som: GetBlogPostSOM) -> GetBlogPostRes:
    return GetBlogPostRes(
      user_id=blog_post_som.user_id,
      id=blog_post_som.id,
      title=blog_post_som.title,
      body=blog_post_som.body
    )
