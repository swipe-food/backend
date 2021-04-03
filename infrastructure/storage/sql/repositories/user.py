from typing import List, Callable
from uuid import UUID

from domain.exceptions import InvalidValueException
from domain.model.user_aggregate import User
from domain.repositories.user import AbstractUserRepository
from infrastructure.storage.sql.model import DBUser, DBUserLanguages, DBUserSeenRecipes
from infrastructure.storage.sql.postgres import PostgresDatabase
from infrastructure.storage.sql.repositories.decorators import catch_no_result_found_exception, catch_add_data_exception, catch_update_data_exception, catch_delete_data_exception


def create_user_repository(database: PostgresDatabase, create_logger: Callable):
    if not isinstance(database, PostgresDatabase):
        raise InvalidValueException(UserRepository, 'database must be a PostgresDatabase')
    return UserRepository(database=database, create_logger=create_logger)


class UserRepository(AbstractUserRepository):

    def __init__(self, database: PostgresDatabase, create_logger: Callable):
        self._db = database
        self._logger = create_logger(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')

    @catch_add_data_exception
    def add(self, entity: User):
        self._db.add(DBUser.from_entity(entity))
        self._logger.debug("added user to database", user_id=entity.id.__str__())

    @catch_add_data_exception
    def add_languages(self, user: User):
        db_user_languages = [DBUserLanguages.from_entity(user, lang) for lang in user.languages]
        self._db.add(*db_user_languages)
        self._logger.debug("added languages of user to database", user_id=user.id.__str__())

    @catch_add_data_exception
    def add_seen_recipes(self, user: User):
        db_user_seen_recipes = [DBUserSeenRecipes.from_entity(user, recipe) for recipe in user.seen_recipes]
        self._db.add(*db_user_seen_recipes)
        self._logger.debug("added seen recipes of user to database", user_id=user.id.__str__())

    @catch_no_result_found_exception
    def get_by_email(self, email: str) -> User:
        db_user: DBUser = self._db.session.query(DBUser).filter(DBUser.email == email).one()
        user = db_user.to_entity()
        self.load_relationship_for_user(db_user, user)
        self._logger.debug("get user by email", user_id=user.id.__str__())
        return user

    @catch_no_result_found_exception
    def get_by_id(self, entity_id: UUID) -> User:
        db_user: DBUser = self._db.session.query(DBUser).filter(DBUser.id == entity_id).one()
        user = db_user.to_entity()
        self.load_relationship_for_user(db_user, user)
        self._logger.debug("get user by id", user_id=user.id.__str__())
        return user

    @catch_no_result_found_exception
    def get_all(self, limit: int = None) -> List[User]:
        db_users: List[DBUser] = self._db.session.query(DBUser).limit(limit).all()
        users: List[User] = []
        for db_user in db_users:
            user = db_user.to_entity()
            self.load_relationship_for_user(db_user, user)
            users.append(user)
        self._logger.debug("get all users", limit=limit, count=len(users))
        return users

    @catch_update_data_exception
    def update(self, entity: User):
        self._db.update(table=DBUser, filters=(DBUser.id == entity.id,), data={
            DBUser.name: entity.name,
            DBUser.first_name: entity.first_name,
            DBUser.is_confirmed: entity.is_confirmed,
            DBUser.date_last_login: entity.date_last_login,
            DBUser.email: entity.email,
        })
        self._logger.debug("updated user", user_id=entity.id.__str__())

    @catch_delete_data_exception
    def delete(self, entity: User):
        self._db.delete(table=DBUser, filters=(DBUser.id == entity.id,))
        self._logger.debug("deleted user", user_id=entity.id.__str__())

    @staticmethod
    def load_relationship_for_user(db_user: DBUser, user: User):
        for liked_category in db_user.liked_categories:
            user.add_category_like(liked_category.to_entity())
        for match in db_user.matches:
            user.add_match(match.to_entity())
