from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text, DECIMAL
from infrastructure.databases.base import Base

class Vouchers(Base):
    __tablename__ = 'vouchers'
    __table_args__ = {'extend_existing': True}

    voucher_id = Column(String(255), primary_key=True)
    voucher_code = Column(String(100), unique=True, nullable=False)
    voucher_name = Column(String(255), nullable=False)
    description = Column(Text)
    discount_type = Column(String(50), nullable=False)
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    min_order_amount = Column(DECIMAL(10, 2))
    points_required = Column(Integer)
    max_uses_per_user = Column(Integer)
    total_quantity = Column(Integer, nullable=False)
    used_quantity = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)