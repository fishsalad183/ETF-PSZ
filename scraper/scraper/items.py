# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item

class VoziloItem(Item):
    url = Field()
    naslov = Field()
    cena = Field()
    stanje = Field()
    marka = Field()
    model = Field()
    godiste = Field()
    kilometraza = Field()
    karoserija = Field()
    gorivo = Field()
    kubikaza = Field()
    snaga = Field()
    menjac = Field()
    vrata = Field()
    boja = Field()
    lokacija_prodavca = Field()

# class NekretninaItem(Item):
#     url = Field()
#     naslov = Field()
#     tip = Field()
#     ponuda = Field()
#     cena = Field()
#     grad = Field()
#     deo_grada = Field()
#     kvadratura = Field()
#     stanje = Field()
#     godina_izgradnje = Field()
#     povrsina_zemljista = Field()
#     sprat = Field()
#     spratnost = Field()
#     opremljenost = Field()
#     uknjizeno = Field()
#     grejanje = Field()
#     broj_soba = Field()
#     broj_kupatila = Field()
#     parking = Field()
#     lift = Field()
#     terasa = Field()
