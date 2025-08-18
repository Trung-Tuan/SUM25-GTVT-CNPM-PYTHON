from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float , Text
from infrastructure.databases.base import Base

class ShippingTracking(Base):
    __tablename__ = 'shipping_tracking'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)

    tracking_number = Column(String(100), nullable=False)
    shipping_status = Column(String(50), nullable=False)  # 'pending', 'shipped', 'delivered', 'returned'
    shipped_date = Column(DateTime)
    delivery_date = Column(DateTime)
    carrier = Column(String(100), nullable=False)  # Ví dụ: 'GrabExpress', 'J&T Express'

    order_id = Column(Integer, ForeignKey('orders.id')) # Liên kết với đơn hàng