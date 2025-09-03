from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float , Text
from infrastructure.databases.base import Base

class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)

    total_amount = Column(Float)
    deposit_amount = Column(Float)
    discount_amount = Column(Float)
    final_amount = Column(Float)
    payment_status = Column(String(50), nullable=False)  # 'pending', 'paid', 'failed'  
    order_type = Column(String(50), nullable=False)  # 'rent', 'buy'
    retal_start_date = Column(DateTime)
    rental_end_date = Column(DateTime)
    expected_return_date = Column(DateTime)
    actual_return_date = Column(DateTime)
    order_status = Column(String(50), nullable=False)  # 'pending', 'completed', 'cancelled'
    shipping_address = Column(String(255))
    created_at = Column(DateTime, nullable=False)

    renter_id = Column(Integer, ForeignKey('Users.id'))  # Người thuê
    supplier_id = Column(Integer, ForeignKey('Users.id'))  # Người cung cấp