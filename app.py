from fastapi import FastAPI
from article.router import router as article_router
from auth.router import router as auth_router
from bookmark.router import router as bookmark_router
from category.router import router as category_router
from comments.router import router as comment_router
from complaint.router import router as complaint_router
from media.router import router as media_router


article_router.include_router(comment_router)
article_router.include_router(media_router)

app = FastAPI()
app.include_router(auth_router)
app.include_router(article_router)
app.include_router(bookmark_router)
app.include_router(category_router)
app.include_router(complaint_router)

