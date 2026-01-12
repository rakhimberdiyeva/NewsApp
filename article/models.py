
from sqlalchemy import Column, String, Text, BigInteger, ForeignKey, DateTime

from core.models import Base, IntIdMixin, TimeActionMixin

class Article(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = 'articles'

    title = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(BigInteger, ForeignKey('categories.id', ondelete="SET NULL"), nullable=True)
    author_id = Column(BigInteger, ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    status = Column(String(20), nullable=False, default='draft')
    published_at = Column(DateTime, nullable=True)

