from __future__ import annotations

import uuid
from typing import List

from domain.exceptions import InvalidValueException
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
from domain.repositories.category import AbstractCategoryRepository
from domain.services.category import AbstractCategoryService


def create_category_service(category_repo: AbstractCategoryRepository) -> CategoryService:
    if not isinstance(category_repo, AbstractCategoryRepository):
        raise InvalidValueException(CategoryService, 'category_repo must be a AbstractCategoryRepository')
    return CategoryService(repo=category_repo)


class CategoryService(AbstractCategoryService):

    def __init__(self, repo: AbstractCategoryRepository):
        self._repo = repo

    def get_by_id(self, category_id: uuid.UUID) -> Category:
        return self._repo.get_by_id(category_id)

    def get_by_name(self, vendor_name: str) -> Category:
        return self._repo.get_by_name(vendor_name)

    def get_all(self, limit: int) -> List[Category]:
        return self._repo.get_all(limit)

    def get_recipes(self, category_id: uuid.UUID, limit: int or None) -> List[Recipe]:
        category = self._repo.get_by_id(category_id)

        return self._repo.get_recipes(category, limit)

    def get_liked_users(self, category_id: uuid.UUID) -> List[User]:
        category = self._repo.get_by_id(category_id)

        return self._repo.get_liked_users(category)
