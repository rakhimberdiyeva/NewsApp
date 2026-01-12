from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, String, Text, Boolean

from core.models import Base, IntIdMixin, TimeActionMixin

class Category(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = 'categories'

    name = Column(String(320), nullable=False)
    description = Column(String(2048), nullable=False)




