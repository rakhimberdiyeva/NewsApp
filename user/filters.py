from fastapi_filter.contrib.sqlalchemy import Filter

from auth.models import User


class UserFilter(Filter):
    fullname: str | None = None
    role: str | None = None

    class Constants(Filter.Constants):
        model = User
        search_field_name = 'q',
        search_model_fields = ["username"]