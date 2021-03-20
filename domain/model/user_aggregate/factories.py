from datetime import datetime
from typing import List

from domain.model.category_aggregate import Category
from domain.model.common_aggregate import Language
from domain.model.user_aggregate.entities import User, CategoryLike
from domain.model.user_aggregate.value_objects import EMail


def create_user(name: str, first_name: str, email: str, is_confirmed: bool, date_last_login: datetime,
                languages: List[Language]) -> User:
    return User(
        name=name,
        first_name=first_name,
        email=EMail(email),
        is_confirmed=is_confirmed,
        date_last_login=date_last_login,
        languages=languages,
    )


def create_category_like(user: User, category: Category, views: int, matches: int) -> CategoryLike:
    return CategoryLike(
        user=user,
        category=category,
        views=views,
        matches=matches
    )
