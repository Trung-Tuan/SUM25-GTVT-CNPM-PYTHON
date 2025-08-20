from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text, DECIMAL
from infrastructure.databases.base import Base

class Revenues(Base):
    __tablename__ = 'revenues'
    __table_args__ = {'extend_existing': True}

    revenue_id = Column(Integer, primary_key=True)
    revenue_type = Column(String(100), nullable=False)
    gross_amount = Column(DECIMAL(10, 2), nullable=False)
    platform_fee = Column(DECIMAL(10, 2), nullable=False)
    net_amount = Column(DECIMAL(10, 2), nullable=False)
    fee_percentage = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(String(100), nullable=False)
    payout_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False)

    supplier_id = Column(Integer, ForeignKey('flask_user.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))