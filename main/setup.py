from datetime import datetime
from uuid import uuid4

from domain.model.language_aggregate import create_language
from domain.model.vendor_aggregate import create_vendor
from infrastructure.config import create_new_config
from infrastructure.log import Logger
from infrastructure.storage.sql.postgres import create_postgres_database
from infrastructure.storage.sql.repositories.language import create_language_repository
from infrastructure.storage.sql.repositories.vendor import create_vendor_repository

if __name__ == '__main__':
    config = create_new_config()

    db = create_postgres_database(config.database, Logger.create)
    language_repo = create_language_repository(db, Logger.create)
    vendor_repo = create_vendor_repository(db, Logger.create)

    german = create_language(uuid4(), name='german', code='DE')
    language_repo.add(german)

    chefkoch = create_vendor(uuid4(), name='Chefkoch', description='...', url='https://www.chefkoch.de', is_active=True, recipe_pattern='', date_last_crawled=datetime.now(),
                             categories_link='https://www.chefkoch.de/rezepte/kategorien/', language=german, categories=[])
    vendor_repo.add(chefkoch)
