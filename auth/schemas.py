from enum import Enum
import re
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


class RoleEnum(Enum):
    client = "client"
    admin = "admin"
    moderator = "moderator"
    author = "author"


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=320)
    fullname: str = Field(min_length=3, max_length=512)
    email: EmailStr

    @field_validator("username", mode="before")
    @classmethod
    def lower_username(cls, value):
        return value.lower()


class RegisterUser(UserBase):
    password1: str
    password2: str

    @field_validator("password1", "password2", mode="before")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Пароль должен состоять из 8 символов")
        if not re.search(r"[A-ZА-Я]", value):
            raise ValueError("Пароль должен состоять хотя бы из одной заглавной буквы")
        if not re.search(r"[a-zа-я]", value):
            raise ValueError("Пароль должен состоять хотя бы из одной строчной буквы")
        if not re.search(r"[0-9]", value):
            raise ValueError("Пароль должен состоять хотя бы из одной цифры")
        if not re.search(r"[\W_]", value):
            raise ValueError("Пароль должен состоять хотя бы из одного спец символа")
        return value


    @model_validator(mode="after")
    def check_password_match(self):
        if self.password1 != self.password2:
            raise ValueError("Пароли не совпадают")
        return self
