from sqlalchemy import Column, Integer, String, DateTime, Boolean
from infrastructure.databases.base import Base

class User(Base):
    __tablename__ = 'flask_user'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    user_name = Column(String(18), nullable=False,unique= True)
    password = Column(String(18), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(12), nullable=True)
    address = Column(String(255), nullable=True)
    is_verified = Column(Boolean, nullable=False)
    user_type = Column(String(50), nullable=False)  # 'renter' , 'supplier', 'admin'
    reward_points = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False) 