from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text
from infrastructure.databases.base import Base

class Reviews(Base):
    __tablename__ = 'reviews'
    __table_args__ = {'extend_existing': True}

    review_id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    review_type = Column(String(50))
    is_verified = Column(Boolean)
    created_at = Column(DateTime, nullable=False)

    reviewer_id = Column(Integer, ForeignKey('Users.id'))
    reviewed_id = Column(Integer, ForeignKey('Users.id'))
    toy_id = Column(Integer, ForeignKey('toys.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))