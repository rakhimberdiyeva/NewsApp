from sqlalchemy import BigInteger, Column, DateTime, String, Text, Boolean

from core.models import Base, IntIdMixin, TimeActionMixin

class User(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = 'users'

    username = Column(String(320), unique=True, nullable=False)
    fullname = Column(String(512), nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String(20), nullable=False, default="client")
    is_active = Column(Boolean, default=True)
    avatar = Column(String, nullable=True)



