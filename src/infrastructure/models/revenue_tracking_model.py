from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text, DECIMAL
from infrastructure.databases.base import Base

class Revenues(Base):
    __tablename__ = 'revenues'
    __table_args__ = {'extend_existing': True}

    revenue_id = Column(String(255), primary_key=True)
    supplier_id = Column(String(255), nullable=False)
    order_id = Column(String(255), nullable=False)
    revenue_type = Column(String(100), nullable=False)
    gross_amount = Column(DECIMAL(10, 2), nullable=False)
    platform_fee = Column(DECIMAL(10, 2), nullable=False)
    net_amount = Column(DECIMAL(10, 2), nullable=False)
    fee_percentage = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(String(100), nullable=False)
    payout_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False)

    supplier_id_fk = Column(String(255), ForeignKey('suppliers.id'))
    order_id_fk = Column(String(255), ForeignKey('orders.id'))