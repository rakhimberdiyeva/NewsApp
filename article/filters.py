from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter

from article.models import Article


class ArticleFilter(Filter):
    category_id: int | None = None
    published_at__gte: datetime | None = None
    published_at__lte: datetime | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = Article
        search_field_name = 'q',
        search_model_fields = ["title"]