from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, String, Text, Boolean

from core.models import Base, IntIdMixin, TimeActionMixin

class Category(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = 'categories'

    name = Column(String(100), nullable=False)
    description = Column(String(512))
    slug = Column(String)
    seo_title = Column(String)
    seo_description = Column(String)



