from application.api.services.category import create_category_service
from application.api.services.status import create_status_service
from application.api.services.vendor import create_vendor_service
from infrastructure.api import SwipeFoodAPI
from infrastructure.config import create_new_config
from infrastructure.log import Logger
from infrastructure.storage.sql.postgres import create_postgres_database
from infrastructure.storage.sql.repositories.category import create_category_repository
from infrastructure.storage.sql.repositories.category_like import create_category_like_repository
from infrastructure.storage.sql.repositories.language import create_language_repository
from infrastructure.storage.sql.repositories.match import create_match_repository
from infrastructure.storage.sql.repositories.recipe import create_recipe_repository
from infrastructure.storage.sql.repositories.user import create_user_repository
from infrastructure.storage.sql.repositories.vendor import create_vendor_repository


def create_api() -> SwipeFoodAPI:
    config = create_new_config()
    Logger.load_config(config.api)
    logger = Logger.create(__name__)

    db = create_postgres_database(config.database, Logger.create)

    category_repo = create_category_repository(db, Logger.create)
    category_like_repo = create_category_like_repository(db, Logger.create)
    language_repo = create_language_repository(db, Logger.create)
    match_repo = create_match_repository(db, Logger.create)
    recipe_repo = create_recipe_repository(db, Logger.create)
    user_repo = create_user_repository(db, Logger.create)
    vendor_repo = create_vendor_repository(db, Logger.create)

    services = dict(
        status=create_status_service(config),
        vendor=create_vendor_service(vendor_repo),
        category=create_category_service(category_repo),
    )

    return SwipeFoodAPI(config=config.api, logger=logger, services=services)


if __name__ == "__main__":
    api = create_api()
    api.run()
