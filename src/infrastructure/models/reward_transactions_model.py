from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from infrastructure.databases.base import Base

class Transactions(Base):
    __tablename__ = 'reward_transactions'
    __table_args__ = {'extend_existing': True}

    transaction_id = Column(Integer, primary_key=True)
    points_change = Column(Integer, nullable=False)
    transaction_type = Column(String(50), nullable=False)
    reason = Column(Text)
    created_at = Column(DateTime, nullable=False)

    user_id_fk = Column(Integer, ForeignKey('flask_user.id'))
    related_order_id_fk = Column(Integer, ForeignKey('orders.id'))