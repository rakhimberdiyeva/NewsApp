from sqlalchemy import Column, String, BigInteger, ForeignKey

from core.models import TimeActionMixin, IntIdMixin, Base


class Comment(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = "comments"

    body = Column(String(2048), nullable=False)
    article_id = Column(BigInteger, ForeignKey("articles.id", ondelete="CASCADE"))
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
