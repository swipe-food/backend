import os
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

from bs4 import BeautifulSoup
from pytest import fixture

from domain.model.category_aggregate import create_category, Category
from domain.model.ingredient_aggregate import create_ingredient
from domain.model.language_aggregate import Language, create_language
from domain.model.recipe_aggregate import create_recipe, Recipe
from domain.model.vendor_aggregate import create_vendor, Vendor


def load_sample_website(filename: str):
    path = os.path.join(Path(__file__).parent.parent, f'Assets/sample_websites/{filename}')
    with open(path, "rb") as file:
        soup = BeautifulSoup(file.read(), "lxml")
        soup.url = 'https://www.chefkoch.de/rezepte/2529011396359402/Bacon-Bomb.html'
        return soup


@fixture
def language() -> Language:
    return create_language(language_id=uuid4(), name='german', code='DE')


@fixture
def vendor(language: Language) -> Vendor:
    return create_vendor(
        vendor_id=uuid4(),
        name='Chefkoch',
        description='...',
        url='https://www.chefkoch.de',
        is_active=True,
        recipe_pattern='',
        date_last_crawled=datetime.now(),
        categories_link='https://www.chefkoch.de/rezepte/kategorien/',
        language=language,
        categories=[],
    )


@fixture
def category(vendor: Vendor) -> Category:
    return create_category(category_id=uuid4(), name='Party', url='https://www.chefkoch.de/rezepte/kategorien/party', vendor=vendor)


@fixture
def recipe(vendor: Vendor, language: Language, category: Category) -> Recipe:
    return create_recipe(
        recipe_id=uuid4(),
        name='Bacon Bomb',
        description='Bacon Bomb - es wird ein verschließbarer Grill sowie eine Aluschale benötigt. '
                    'Über 87 Bewertungen und für vorzüglich befunden. Mit ► Portionsrechner ► Kochbuch ► Video-Tipps!',
        image_url='https://img.chefkoch-cdn.de/rezepte/2529011396359402/bilder/678972/crop-960x540/bacon-bomb.jpg',
        category=category,
        vendor=vendor,
        url='https://www.chefkoch.de/rezepte/2529011396359402/Bacon-Bomb.html',
        language=language,
        cook_time=timedelta(minutes=10),
        prep_time=timedelta(minutes=10),
        total_time=timedelta(minutes=10),
        author='Chefkoch-Video',
        ingredients=[
            create_ingredient(ingredient_id=uuid4(), text='16 Scheibe/n Frühstücksspeck'),
            create_ingredient(ingredient_id=uuid4(), text='1 kg Hackfleisch , gemischtes'),
            create_ingredient(ingredient_id=uuid4(), text='2  Zwiebel(n)'),
            create_ingredient(ingredient_id=uuid4(), text='200 g Gouda , geriebener'),
            create_ingredient(ingredient_id=uuid4(), text=' BBQ-Sauce'),
            create_ingredient(ingredient_id=uuid4(), text='1 TL Salz'),
            create_ingredient(ingredient_id=uuid4(), text='1 EL Pfeffer'),
            create_ingredient(ingredient_id=uuid4(), text='1 EL Zwiebelgranulat'),
            create_ingredient(ingredient_id=uuid4(), text='1 EL Knoblauchgranulat'),
        ],
        date_published=datetime(year=2014, month=4, day=13),
        rating_count=87,
        rating_value=4.49,
    )
