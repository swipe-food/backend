import os
from pathlib import Path

from bs4 import BeautifulSoup

from plugins.crawler.scrapers import ParsedRecipe


def load_sample_website(filename: str):
    path = os.path.join(Path(__file__).parent.parent.parent, f'Assets/sample_websites/{filename}')
    with open(path, "rb") as file:
        return BeautifulSoup(file.read(), "lxml")


parsed_recipe_sample = ParsedRecipe({
    'name': 'Bacon Bomb',
    'description': 'Bacon Bomb - es wird ein verschließbarer Grill sowie eine Aluschale benötigt. '
                   'Über 87 Bewertungen und für vorzüglich befunden. Mit ► Portionsrechner ► Kochbuch ► Video-Tipps!',
    'image': 'https://img.chefkoch-cdn.de/rezepte/2529011396359402/bilder/678972/crop-960x540/bacon-bomb.jpg',
    'recipeCategory': 'Party',
    'recipeIngredient': [
        '16 Scheibe/n Frühstücksspeck', '1 kg Hackfleisch , gemischtes', '2  Zwiebel(n)', '200 g Gouda , geriebener',
        ' BBQ-Sauce', '1 TL Salz', '1 EL Pfeffer', '1 EL Zwiebelgranulat', '1 EL Knoblauchgranulat'
    ],
    'recipeInstructions': 'Zuerst ein Netz aus dem Frühstücksspeck erstellen. Dazu zuerst 6 - 8 Speckstreifen nebeneinander legen, dabei jeweils eine Speckstreifenbreite frei lassen. Dann 6 - 8 Streifen quer dazu legen und ein enges Netz daraus flechten.Die Gewürze zum BBQ-Rub vermischen. Das Hackfleisch mit dem BBQ-Rub verkneten. Die Hackfleischmasse auf dem Specknetz verteilen. Dann die Zwiebel in Ringe schneiden und darauf verteilen und andrücken. Darauf eine Schicht geriebenen Gouda streuen. Wer es gerne scharf mag, kann Peperoni, Jalapeños oder grob geschroteten Pfeffer darauf streuen. Dann alles vorsichtig zu einer Rolle formen. Damit die Bacon Bomb nicht auf dem Grillrost anbrennt, eine Aluschale umgekehrt auf den Grill legen und darauf dann die Bacon Bomb platzieren. 30 bis 40 Min. indirekt grillen. Nach dem Grillen BBQ-Sauce auf die Bacon Bomb geben.',
    'datePublished': '2014-04-13',
    'author': {'name': 'Chefkoch-Video'},
    'aggregateRating': {'ratingCount': 87, 'ratingValue': 4.49}
})
