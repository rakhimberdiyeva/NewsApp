from fastapi_filter.contrib.sqlalchemy import Filter

from category.models import Category


class CategoryFilter(Filter):
    q: str | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = Category
        search_field_name = 'q'
        search_model_fields = ["name"]

