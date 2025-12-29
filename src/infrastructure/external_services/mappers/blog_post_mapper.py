from domain.core.blog_post import BlogPost
from infrastructure.external_services.dto.res.blog_post_ext_res import BlogPostExtRes


class BlogPostMapper:
  @staticmethod
  def ext_res_to_domain(blog_post_ext_res: BlogPostExtRes) -> BlogPost:
    return BlogPost(
      user_id=blog_post_ext_res.user_id,
      id_=blog_post_ext_res.id,
      title=blog_post_ext_res.title,
      body=blog_post_ext_res.body
    )
