import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import BigInteger, Column, DateTime
class Base(DeclarativeBase):
    pass


class IntIdMixin:
    id = Column(BigInteger, primary_key=True, autoincrement=True)

class TimeActionMixin:
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)