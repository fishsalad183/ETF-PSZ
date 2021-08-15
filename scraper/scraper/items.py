# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
from scrapy.item import Field, Item
from scrapy.loader.processors import MapCompose


def remove_whitespace(text):
    return text.strip()

def only_numeric_characters(text):
    return re.sub("[^0-9]", "", text)

class NekretninaItem(Item):
    naslov = Field(
        input_processor=MapCompose(remove_whitespace)
    )
    cena = Field(
        input_processor=MapCompose(only_numeric_characters)
    )
    ponuda = Field(
        # input_processor=MapCompose()
    )
    tip = Field()
    grad = Field()
    deo_grada = Field()
    kvadratura = Field()
    stanje = Field()
    godina_izgradnje = Field()
    povrsina_zemljista = Field()
    sprat = Field()
    spratnost = Field()
    opremljenost = Field()
    uknjizeno = Field()
    grejanje = Field()
    broj_soba = Field()
    broj_kupatila = Field()
    parking = Field()
    lift = Field()
    terasa = Field()


