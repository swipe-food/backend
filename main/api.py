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

if __name__ == "__main__":
    config = create_new_config()
    Logger.load_config(config.log_file_name)
    logger = Logger.create(__name__)

    db = create_postgres_database(config.database, Logger.create)
    category_repo = create_category_repository(db, Logger.create)
    category_like_repo = create_category_like_repository(db, Logger.create)
    language_repo = create_language_repository(db, Logger.create)
    match_repo = create_match_repository(db, Logger.create)
    recipe_repo = create_recipe_repository(db, Logger.create)
    user_repo = create_user_repository(db, Logger.create)
    vendor_repo = create_vendor_repository(db, Logger.create)
