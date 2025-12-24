from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt, JWTError

from auth.models import User
from auth.schemas import Token
from core.settings import TIMEZONE, REFRESH_TIME, ACCESS_TIME, SECRET_KEY


class TokenServices:
    def __generate_token(self, user: User, is_refresh: bool = False) -> str:
        exp = datetime.now(tz=TIMEZONE) + (
            timedelta(hours=int(REFRESH_TIME)) if is_refresh else timedelta(hours=int(ACCESS_TIME))
        )
        token = jwt.encode(
            {
                "sub": str(user.id),
                "username": user.username,
                "exp": exp,
                "refresh": is_refresh,
            },
            SECRET_KEY,
            "HS256"
        )
        return token

    def generate(self, user: User) -> Token:
        access_token = self.__generate_token(user)
        refresh_token = self.__generate_token(user, True)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )

    def __validate_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        except JWTError:
            raise HTTPException(401, "Invalid credentials")


    def validate(self, token: str, is_refresh: bool = False) -> dict:
        payload = self.__validate_token(token)
        if is_refresh is True and bool(payload.get("refresh")) is False:
            raise HTTPException(401, "Invalid credentials")
        return payload

