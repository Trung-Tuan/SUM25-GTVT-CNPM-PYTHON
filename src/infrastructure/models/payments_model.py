from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Text, DECIMAL
from infrastructure.databases.base import Base

class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = {'extend_existing': True}

    id = Column(String(255), primary_key=True)
    
    payment_method = Column(String(50), nullable=False)
    payment_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(String(50), nullable=False)
    transaction_id = Column(String(100))
    platform_fee = Column(DECIMAL(10, 2))
    supplier_earnings = Column(DECIMAL(10, 2))
    payment_date = Column(DateTime, nullable=False)
    refund_amount = Column(DECIMAL(10, 2))
    refund_date = Column(DateTime)

    order_id = Column(String(255), ForeignKey('orders.id'))