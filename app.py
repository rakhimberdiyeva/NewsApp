from fastapi import FastAPI
from auth.router import router as auth_router
from category.router import router as category_router
from article.router import router as article_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(article_router)
app.include_router(category_router)