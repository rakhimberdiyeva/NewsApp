from sqlalchemy import Column, String, BigInteger, ForeignKey, Text

from complaint.schemas import ComplaintStatusEnum
from core.models import Base, IntIdMixin, TimeActionMixin


class Complaint(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = "complaints"

    target_type = Column(String(20), nullable=False)
    target_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(100), default=ComplaintStatusEnum.new)
