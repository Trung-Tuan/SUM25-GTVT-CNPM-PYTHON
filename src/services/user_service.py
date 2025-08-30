from domain.models.user import User
from domain.models.iuser_repository import IUserRepository
from typing import Optional
class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def login(self, user_name: str, password: str) -> Optional[User]:
        if not user_name or not password:
            return None

        user = self.repository.get_by_user_name(user_name)
        if not user:
            return None
        
        if user.password != password:
            return None
        return user
    
    def register(self, user_name: str, password: str, email: str) -> Optional[User]:
        if self.repository.get_by_user_name(user_name):
            return None 
        
        new_user = User(user_name=user_name, password=password, email=email)
        return self.repository.add(new_user)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)
    
    def get_user_by_name(self, user_name: str) -> Optional[User]:
        return self.repository.get_by_user_name(user_name)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_by_user_email(email)
    
    def update_user(
        self,
        user_id: int,
        user_name: str,
        full_name: str,
        password: str,
        address: str,
        email: str,
        phone_number: str,
        role_name: str
    ) -> Optional[object]:
        
        existing_user = self.repository.get_by_id(user_id)
        if not existing_user:
            return None
        existing_user.user_name = user_name
        existing_user.full_name = full_name
        existing_user.password = password
        existing_user.address = address
        existing_user.email = email
        existing_user.phone_number = phone_number
        existing_user.role_name = role_name
        return self.repository.update(existing_user)