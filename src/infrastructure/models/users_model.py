from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from infrastructure.databases.base import Base

class UserModel(Base):
    __tablename__ = 'Users'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False,unique= True)
    password = Column(String(30), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(12), nullable=True)
    address = Column(String(255), nullable=True)
    is_verified = Column(Boolean, nullable=True, default=False)
    user_type = Column(String(50), nullable=False, default="renter")  # 'renter' , 'supplier', 'admin'
    reward_points = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 