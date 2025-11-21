from infrastructure.external_services.typicode.dto.res.blog_post_ext_res import BlogPostExtRes
from services.models.outputs.get_blog_post_som import GetBlogPostSOM


class GetBlogPostMapper:
  @staticmethod
  def blog_post_ext_res_to_som(blog_post_ext_res: BlogPostExtRes) -> GetBlogPostSOM:
    return GetBlogPostSOM(
      user_id=blog_post_ext_res.user_id,
      id=blog_post_ext_res.id,
      title=blog_post_ext_res.title,
      body=blog_post_ext_res.body
    )
