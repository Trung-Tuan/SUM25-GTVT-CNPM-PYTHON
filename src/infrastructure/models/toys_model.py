from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float , Text, Boolean, NVARCHAR
from infrastructure.databases.base import Base

class Toys(Base):
    __tablename__ = 'toys'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(NVARCHAR(255), nullable=False)
    description = Column(NVARCHAR(255))
    min_age = Column(Integer)
    max_age = Column(Integer)


    toy_name = Column(NVARCHAR(255), nullable=False)
    brand = Column(NVARCHAR(255))

    total_quantity = Column(Integer, nullable=False)
    available_quantity = Column(Integer, nullable=False)

    price_sale = Column(Float)
    price_1_day = Column(Float)
    price_1_week = Column(Float)
    price_2_weeks = Column(Float)

    is_active = Column(Integer, nullable=False)  
    is_for_sale = Column(Boolean, nullable=False)
    is_for_rent = Column(Boolean, nullable=False)

    status = Column(NVARCHAR(255), nullable=False)  # 'available', 'rented', 'sold'
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 

    category = Column(NVARCHAR(255))
    image = Column(String(255))
    rating = Column(Float)
    reviews = Column(Integer)


