from sqlalchemy import Column, Integer, ForeignKey, BigInteger, UniqueConstraint

from core.models import Base, IntIdMixin, TimeActionMixin


class Bookmark(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = "bookmarks"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(BigInteger, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)



    __table_args__ = (
        UniqueConstraint("user_id", "article_id"),
    )
