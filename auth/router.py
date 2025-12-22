from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.manager import AuthManager
from auth.schemas import RegisterUser
from core.session import async_session

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register")
async def register(request: RegisterUser):
    async with async_session() as session:
        manager = AuthManager(session)
        await manager.register(request)
        return {"status": "success"}


@router.post("/login")
async def login(
        request: OAuth2PasswordRequestForm = Depends(),
):
    async with async_session() as session:
        manager = AuthManager(session)
        response = await manager.login(request.username, request.password)
        return response


