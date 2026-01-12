from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.manager import AuthManager
from auth.models import User
from auth.schemas import RegisterUser, RefeshToken
from core.dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register")
async def register(request: RegisterUser, db: AsyncSession = Depends(get_db)): # установили зависимость. пока сессию не создали у нас нет доступа к эндпоинту
    manager = AuthManager(db)
    await manager.register(request)
    return {"status": "success"}


@router.post("/login")
async def login(
        request: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    manager = AuthManager(db)
    response = await manager.login(request.username, request.password)
    return response


@router.post("/refresh")
async def refresh(request: RefeshToken, db: AsyncSession = Depends(get_db)):
    manager = AuthManager(db)
    response = await manager.refresh(request)
    return response


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user