from domain.models.iuser_repository import IUserRepository
from infrastructure.models.users_model import User
from sqlalchemy.orm import Session
from typing import Optional, List


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.commit() # lưu vào DB
        self.session.refresh(user) 
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()
    
    def get_by_user_name(self, user_name: str) -> Optional[User]:
        return self.session.query(User).filter(User.user_name == user_name).first()
    
    def get_by_user_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first() # SELECT * FROM users WHERE email = 'email_value'  LIMIT 1;
    
    def list(self) -> List[User]:
        return self.session.query(User).all() # SELECT * FROM users;
    
    def update(self, user: User) -> User:
        self.session.merge(user) # update hoặc insert
        self.session.commit()
        return user
    
    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
