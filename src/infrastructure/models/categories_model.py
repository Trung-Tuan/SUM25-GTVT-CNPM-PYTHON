from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float , Text
from infrastructure.databases.base import Base

class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False)
    description = Column(Text)
    min_age = Column(Integer)
    max_age = Column(Integer)
    is_active = Column(Integer, nullable=False)  
    