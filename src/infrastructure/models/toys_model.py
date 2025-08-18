from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float , Text, Boolean
from infrastructure.databases.base import Base

class Toys(Base):
    __tablename__ = 'toys'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False)
    description = Column(Text)
    min_age = Column(Integer)
    max_age = Column(Integer)
    is_active = Column(Integer, nullable=False)  
    toy_name = Column(String(255), nullable=False)
    brand = Column(String(255))
    total_quantity = Column(Integer, nullable=False)
    available_quantity = Column(Integer, nullable=False)
    price_sale = Column(Float)
    price_1_day = Column(Float)
    price_1_week = Column(Float)
    price_2_weeks = Column(Float)
    deposit_amount = Column(Float)
    is_for_sale = Column(Boolean, nullable=False)
    is_for_rent = Column(Boolean, nullable=False)
    status = Column(String(50), nullable=False)  # 'available', 'rented', 'sold'
    created_at = Column(DateTime, nullable=False)
