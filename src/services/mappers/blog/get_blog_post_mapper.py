from domain.core.blog_post import BlogPost
from services.models.outputs.get_blog_post_som import GetBlogPostSOM


class GetBlogPostMapper:
  @staticmethod
  def entity_to_som(entity: BlogPost) -> GetBlogPostSOM:
    return GetBlogPostSOM(
      user_id=entity.user_id,
      id=entity.id,
      title=entity.title,
      body=entity.body
    )
