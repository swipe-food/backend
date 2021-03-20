from typing import List, Tuple

from domain.model.entity import Entity
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import CategoryLike
from domain.model.vendor_aggregate import Vendor


class Category(Entity):

    def __init__(self, name: str, vendor: Vendor):
        super().__init__()

        self.name = name
        self.vendor = vendor

        self._likes: List[CategoryLike] = []
        self._recipes: List[Recipe] = []

        self._vendor.add_category(self)

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, value: str):
        self._check_not_discarded()
        if not isinstance(value, str):
            raise ValueError('category name must be a string')
        self._name = value
        self._increment_version()

    @property
    def vendor(self) -> Vendor:
        self._check_not_discarded()
        return self._vendor

    @vendor.setter
    def vendor(self, value: Vendor):
        self._check_not_discarded()
        if not isinstance(value, Vendor):
            raise ValueError('vendor must be a Vendor instance')
        self._vendor = value
        self._increment_version()

    @property
    def likes(self) -> Tuple[CategoryLike]:
        self._check_not_discarded()
        return tuple(self._likes)

    def add_like(self, category_like: CategoryLike):
        self._check_not_discarded()
        if not isinstance(category_like, CategoryLike):
            raise ValueError('category like must be a CategoryLike instance')
        self._likes.append(category_like)
        self._increment_version()

    def remove_like(self, category_like):
        self._check_not_discarded()
        if not isinstance(category_like, CategoryLike):
            raise ValueError('category like must be a CategoryLike instance')
        self._likes.remove(category_like)
        self._increment_version()

    @property
    def recipes(self) -> Tuple[Recipe]:
        self._check_not_discarded()
        return tuple(self._recipes)

    def add_recipe(self, recipe: Recipe):
        self._check_not_discarded()
        if not isinstance(recipe, Recipe):
            raise ValueError('recipe must be an Recipe instance')
        self._recipes.append(recipe)
        self._increment_version()

    def remove_recipe(self, recipe):
        self._check_not_discarded()
        if not isinstance(recipe, Recipe):
            raise ValueError('recipe must be an Recipe instance')
        self._recipes.remove(recipe)
        self._increment_version()

    def delete(self):
        self._vendor.remove_category(self)
        for like in self._likes:
            like.delete()
        for recipe in self._recipes:
            recipe.delete()
        super().delete()

    def __str__(self) -> str:
        return f"Category '{self._name}' of Vendor '{self._vendor.name}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r}, {vendor})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
            vendor=self._vendor.__repr__()
        )
