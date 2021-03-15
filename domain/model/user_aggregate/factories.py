from datetime import datetime
from typing import List

from domain.model.category_aggregate.entities import Category
from domain.model.common_aggregate import Language, create_entity_id
from domain.model.user_aggregate.entities import User, CategoryLike
from domain.model.user_aggregate.value_objects import EMail


def create_user(version: int, name: str, first_name: str, email: str, is_confirmed: bool, date_last_login: datetime,
                languages: List[Language]) -> User:
    return User(user_id=create_entity_id(),
                user_version=version,
                name=name,
                first_name=first_name,
                email=EMail.from_text(email),
                is_confirmed=is_confirmed,
                date_last_login=date_last_login,
                languages=languages)


def create_category_like(version: int, user: User, category: Category, views: int,
                         matches: int) -> CategoryLike:
    return CategoryLike(liked_category_id=create_entity_id(),
                        liked_category_version=version,
                        user=user,
                        category=category,
                        views=views,
                        matches=matches)
