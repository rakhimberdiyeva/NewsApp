from sqlalchemy import select, insert

from passlib.hash import argon2

from auth.models import User
from auth.schemas import RegisterUser
from core.manager import BaseManager


class AuthManager(BaseManager):
    async def check_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        result = result.scalar_one_or_none()
        return True if not result else False

    async def register(self, request: RegisterUser):
        if not self.check_username(request.username):
            pass
        data = request.model_dump()
        data.pop("password2")
        password = argon2.hash(data.pop("password1"))
        stmt = insert(User).values(
            **data,
            password=password
        )
        await self.db.execute(stmt)
        await self.db.commit()


    async def login(self, username:str, password:str):
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            pass
        if not argon2.verify(password, user.password):
            pass
        return user






