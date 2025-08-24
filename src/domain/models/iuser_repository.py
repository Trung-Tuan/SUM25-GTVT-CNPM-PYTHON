from abc import ABC, abstractmethod
from .user import User
from typing import List, Optional

class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_user_name(self, user_name: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_user_email(self, email: str) ->Optional[User]:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass 