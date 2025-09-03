from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float , Text
from infrastructure.databases.base import Base

class Verifications(Base):
    __tablename__ = 'toy_verifications'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)

    verification_status = Column(String(50), nullable=False)  # 'pending', 'approved', 'rejected'
    verification_notes = Column(Text)
    verified_by = Column(String(255))  # Người thực hiện xác minh
    verified_at = Column(DateTime)  # Thời gian xác minh

    admin_id = Column(Integer, ForeignKey('Users.id'))   
    toy_id = Column(Integer, ForeignKey('toys.id')) 