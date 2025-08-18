from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text
from infrastructure.databases.base import Base

class Reviews(Base):
    __tablename__ = 'reviews'
    __table_args__ = {'extend_existing': True}

    review_id = Column(String(255), primary_key=True)
    reviewer_id = Column(String(255), nullable=False)
    reviewed_id = Column(String(255), nullable=False)
    toy_id = Column(String(255))
    order_id = Column(String(255))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    review_type = Column(String(50))
    is_verified = Column(Boolean)
    created_at = Column(DateTime, nullable=False)

    reviewer_id_fk = Column(String(255), ForeignKey('users.id'))
    reviewed_id_fk = Column(String(255), ForeignKey('users.id'))
    toy_id_fk = Column(String(255), ForeignKey('toys.id'))
    order_id_fk = Column(String(255), ForeignKey('orders.id'))