from interfaces.rest.v1.dto.res.get_blog_post_res import GetBlogPostRes
from shared.blog_post import BlogPost


class GetBlogAdapter:
  @staticmethod
  def external_to_res(blog_post: BlogPost) -> GetBlogPostRes:
    return GetBlogPostRes(
      user_id=blog_post.user_id,
      id=blog_post.id,
      title=blog_post.title,
      body=blog_post.body
    )
