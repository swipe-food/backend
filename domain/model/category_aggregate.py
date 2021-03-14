import uuid

from domain.model.common_aggregate import Entity


class Category(Entity):

    def __init__(self, category_id: uuid.UUID, category_version: int, name: str, vendor):
        super().__init__(category_id, category_version)
        self._name = name
        self._vendor = vendor
        self._likes = []
        self._recipes = []

        self._vendor.add_category(self)

    def __str__(self) -> str:
        return f"Category '{self._name}' of Vendor '{self._vendor.name}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r}, {vendor})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
            vendor=self._vendor.__repr__()
        )

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, value: str):
        self._check_not_discarded()
        self._name = value
        self._increment_version()

    @property
    def vendor(self):
        self._check_not_discarded()
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        self._check_not_discarded()
        self._vendor = value
        self._increment_version()

    @property
    def likes(self) -> str:
        self._check_not_discarded()
        return self._likes

    @likes.setter
    def likes(self, value):
        self._check_not_discarded()
        self._likes = value
        self._increment_version()

    def add_like(self, category_like):
        self._check_not_discarded()
        self._likes.append(category_like)
        self._increment_version()

    def remove_like(self, category_like):
        self._check_not_discarded()
        self._likes.remove(category_like)  # TODO error handling: raises ValueError
        self._increment_version()

    @property
    def recipes(self):
        self._check_not_discarded()
        return self._recipes

    @recipes.setter
    def recipes(self, value):
        self._check_not_discarded()
        self._recipes = value
        self._increment_version()

    def add_recipe(self, recipe):
        self._check_not_discarded()
        self._recipes.append(recipe)
        self._increment_version()

    def remove_recipe(self, recipe):
        self._check_not_discarded()
        self._recipes.remove(recipe)  # TODO error handling: raises ValueError
        self._increment_version()

    def delete(self):
        self._vendor.remove_category(self)
        for like in self._likes:
            like.delete()
        for recipe in self._recipes:
            recipe.delete()
        super().delete()

