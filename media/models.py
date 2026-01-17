from sqlalchemy import Column, BigInteger, ForeignKey, String

from core.models import IntIdMixin, TimeActionMixin, Base


class ArticleImage(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = "article_image"

    article_id = Column(BigInteger, ForeignKey("articles.id", ondelete="CASCADE"))
    filename = Column(String)
    file_path = Column(String)

