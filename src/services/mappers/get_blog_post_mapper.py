from domain.entities.blog_post import BlogPost
from services.models.outputs.get_blog_post_som import GetBlogPostSOM


class GetBlogPostMapper:
  @staticmethod
  def blog_post_to_som(blog_post: BlogPost) -> GetBlogPostSOM:
    return GetBlogPostSOM(
      user_id=blog_post.user_id,
      id=blog_post.id,
      title=blog_post.title,
      body=blog_post.body
    )
