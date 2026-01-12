from fastapi import FastAPI
from auth.router import router as auth_router
from category.router import router as category_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(category_router)