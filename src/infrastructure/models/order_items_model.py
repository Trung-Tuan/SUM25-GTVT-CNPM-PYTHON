from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float , Text
from infrastructure.databases.base import Base

class OrderItems(Base):
    __tablename__ = 'order_items'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    item_type = Column(String(50), nullable=False)  # 'rent', 'buy'
    return_status = Column(String(50))  # 'pending', 'returned', 'damaged'
    days_overdue = Column(Integer)  # Số ngày quá hạn nếu có
    late_fee = Column(Float)  # Phí quá hạn nếu có
    damage_fee = Column(Float)  # Phí hư hỏng nếu có

    order_id = Column(Integer, ForeignKey('orders.id')) 
    toy_id = Column(Integer, ForeignKey('toys.id'))  