from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from infrastructure.databases.base import Base

class Transactions(Base):
    __tablename__ = 'reward_transactions'
    __table_args__ = {'extend_existing': True}

    transaction_id = Column(String(255), primary_key=True)
    user_id = Column(String(255), nullable=False)
    points_change = Column(Integer, nullable=False)
    transaction_type = Column(String(50), nullable=False)
    related_order_id = Column(String(255))
    reason = Column(Text)
    created_at = Column(DateTime, nullable=False)

    user_id_fk = Column(String(255), ForeignKey('users.id'))
    related_order_id_fk = Column(String(255), ForeignKey('orders.id'))