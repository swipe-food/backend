from __future__ import annotations

from typing import List, Callable
from uuid import UUID

from domain.exceptions import InvalidValueException
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from domain.repositories.vendor import AbstractVendorRepository
from infrastructure.storage.sql.model import DBVendor, DBRecipe
from infrastructure.storage.sql.postgres import PostgresDatabase
from infrastructure.storage.sql.repositories.decorators import catch_add_data_exception, catch_no_result_found_exception, catch_update_data_exception, catch_delete_data_exception


def create_vendor_repository(database: PostgresDatabase, create_logger: Callable) -> VendorRepository:
    if not isinstance(database, PostgresDatabase):
        raise InvalidValueException(VendorRepository, 'database must be a PostgresDatabase')
    return VendorRepository(database=database, create_logger=create_logger)


class VendorRepository(AbstractVendorRepository):

    def __init__(self, database: PostgresDatabase, create_logger: Callable):
        self._db = database
        self._logger = create_logger(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')

    @catch_add_data_exception
    def add(self, entity: Vendor):
        self._db.add(DBVendor.from_entity(entity))
        self._logger.debug("added vendor to database", vendor_id=entity.id.__str__())

    @catch_no_result_found_exception
    def get_by_id(self, entity_id: UUID) -> Vendor:
        db_vendor: DBVendor = self._db.session.query(DBVendor).filter(DBVendor.id == entity_id).one()
        self._logger.debug("get vendor by id", vendor_id=db_vendor.id.__str__())
        return db_vendor.to_entity()

    @catch_no_result_found_exception
    def get_by_name(self, vendor_name: str) -> Vendor:
        db_vendor: DBVendor = self._db.session.query(DBVendor).filter(DBVendor.name == vendor_name).one()
        self._logger.debug("get vendor by name", vendor_id=db_vendor.id.__str__(), vendor_name=vendor_name)
        return db_vendor.to_entity()

    @catch_no_result_found_exception
    def get_recipes(self, vendor: Vendor) -> List[Recipe]:
        db_recipes: List[DBRecipe] = self._db.session.query(DBRecipe).filter(DBRecipe.fk_vendor == vendor.id).one()
        self._logger.debug("get all recipes for vendor", count=len(db_recipes))
        return [db_recipe.to_entity() for db_recipe in db_recipes]

    @catch_no_result_found_exception
    def get_all(self, limit: int = None) -> List[Vendor]:
        db_vendors: List[DBVendor] = self._db.session.query(DBVendor).limit(limit).all()
        self._logger.debug("get all vendors", limit=limit, count=len(db_vendors))
        return [db_vendor.to_entity() for db_vendor in db_vendors]

    @catch_update_data_exception
    def update(self, entity: Vendor):
        self._db.update(table=DBVendor, filters=(DBVendor.id == entity.id,), data={
            DBVendor.name: entity.name,
            DBVendor.description: entity.description,
            DBVendor.url: entity.url,
            DBVendor.is_active: entity.is_active,
            DBVendor.recipe_pattern: entity.recipe_pattern,
            DBVendor.date_last_crawled: entity.date_last_crawled,
            DBVendor.categories_link: entity.categories_link,
        })
        self._logger.debug("updated vendor", vendor_id=entity.id.__str__())

    @catch_delete_data_exception
    def delete(self, entity: Vendor):
        self._db.delete(table=DBVendor, filters=(DBVendor.id == entity.id,))
        self._logger.debug("deleted vendor", vendor_id=entity.id.__str__())
