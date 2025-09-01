from domain.models.iuser_repository import IUserRepository
from domain.models.user import User  # domain entity
from infrastructure.models.users_model import UserModel  # ORM
from sqlalchemy.orm import Session
from typing import Optional, List


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> User:
        user_model = UserModel(
            user_name=user.user_name,
            email=user.email,
            password=user.password
        )
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        return User(
            user_name=user_model.user_name,
            email=user_model.email,
            password=user_model.password
        ) # mapping từ ORM -> domain entity

    def get_by_id(self, user_id: int) -> Optional[User]:
        user_model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return None
        return User(
            id=user_model.id,
            user_name=user_model.user_name,
            email=user_model.email,
            password=user_model.password,
            created_at=user_model.created_at
        )

    def get_by_user_name(self, user_name: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter(UserModel.user_name == user_name).first()
        return User(
            id=user_model.id,
            user_name=user_model.user_name,
            email=user_model.email,
            password=user_model.password,

        ) if user_model else None

    def get_by_user_email(self, email: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter(UserModel.email == email).first()
        return User(
            id=user_model.id,
            user_name=user_model.user_name,
            email=user_model.email,
            password=user_model.password,

        ) if user_model else None

    def list(self) -> List[User]:
        user_models = self.session.query(UserModel).all()
        return [
            User(
                id=u.id,
                user_name=u.user_name,
                email=u.email,
                password=u.password,

            ) for u in user_models
        ]

    def update(self, user: User) -> User:
        user_model = self.session.query(UserModel).filter(UserModel.id == user.id).first()
        if not user_model:
            return None
        user_model.user_name = user.user_name
        user_model.email = user.email
        user_model.password = user.password
        self.session.commit()
        return user

    def delete(self, user_id: int) -> None:
        user_model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if user_model:
            self.session.delete(user_model)
            self.session.commit()
