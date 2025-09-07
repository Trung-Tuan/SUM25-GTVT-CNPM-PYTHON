from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from infrastructure.databases.base import Base
from datetime import datetime

class CartModel(Base):
    __tablename__ = 'carts'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class CartItemModel(Base):
    __tablename__ = 'cart_items'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('toys.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    item_type = Column(String(50), nullable=False, default='buy')  # 'buy' or 'rent'
    rental_days = Column(Integer, nullable=True)
