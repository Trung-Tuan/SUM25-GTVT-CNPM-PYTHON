from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text
from infrastructure.databases.base import Base

class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    message_content = Column(Text, nullable=False)
    message_type = Column(String(50))
    is_support_ticket = Column(Boolean)
    ticket_status = Column(String(50))
    priority = Column(String(20))
    is_read = Column(Boolean)
    sent_at = Column(DateTime, nullable=False)

    sender_id = Column(Integer, ForeignKey('flask_user.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('flask_user.id'), nullable=False)
    related_toy_id = Column(Integer, ForeignKey('toys.id'))
    related_order_id = Column(Integer, ForeignKey('orders.id'))