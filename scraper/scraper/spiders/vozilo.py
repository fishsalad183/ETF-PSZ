import re

from itemloaders.processors import MapCompose, TakeFirst
from ..items import VoziloItem
from itemloaders import ItemLoader
import scrapy
import logging


class VoziloSpider(scrapy.Spider):
    name = 'vozilo'
    allowed_domains = ['polovniautomobili.com']
    start_urls = ['https://www.polovniautomobili.com/auto-oglasi/pretraga?page=1&sort=basic&city_distance=0&showOldNew=all&without_price=1']

    def __init__(self):
        self._vozilo_index = 0

    def parse(self, response):
        vozilo_page_links = response.css('div.textContent a.ga-title::attr(href)')
        vozilo_lokacije = response.css('div.city::text').getall()
        vozilo_lokacije = list(map(lambda text: text.strip(), vozilo_lokacije))
        if len(vozilo_page_links) != len(vozilo_lokacije):
            logging.warn('len(vozilo_page_links) ({}) != vozilo_locations ({})'.format(len(vozilo_page_links), len(vozilo_lokacije)))
        yield from response.follow_all(vozilo_page_links, self.parse_vozilo, cb_kwargs=dict(lokacije=vozilo_lokacije))
        
        pagination_link = response.css('a.js-pagination-next::attr(href)')
        if pagination_link is not None:
            self._vozilo_index = 0
            yield from response.follow_all(pagination_link, self.parse)
    
    def parse_vozilo(self, response, lokacije):
        
        def only_digits(text) -> str:
            return re.sub("[^0-9]", "", text)

        vozilo_loader = ItemLoader(item=VoziloItem(), selector=response)
        
        vozilo_loader.default_output_processor = TakeFirst()
        
        vozilo_loader.add_value('url', response.request.url)
        vozilo_loader.add_css('naslov', 'h1::text', MapCompose(lambda text: text.strip()))
        vozilo_loader.add_css('cena', 'span.priceClassified::text', MapCompose(lambda text: text.strip()))
        
        podaci_raw = response.css('div.divider div.uk-width-1-2::text').getall()
        podaci_raw = list(map(lambda text: text.replace(':', '').strip(), podaci_raw))
        
        def val(label):
            index = podaci_raw.index(label)
            return podaci_raw[index + 1]
        
        vozilo_loader.add_value('stanje', val('Stanje'))
        vozilo_loader.add_value('marka', val('Marka'))
        vozilo_loader.add_value('model', val('Model'))
        vozilo_loader.add_value('godiste', only_digits(val('Godište')))
        vozilo_loader.add_value('kilometraza', only_digits(val('Kilometraža')))
        vozilo_loader.add_value('karoserija', val('Karoserija'))
        vozilo_loader.add_value('gorivo', val('Gorivo'))
        vozilo_loader.add_value('kubikaza', only_digits(val('Kubikaža')))
        vozilo_loader.add_value('snaga', val('Snaga motora'))
        vozilo_loader.add_value('menjac', val('Menjač'))
        vozilo_loader.add_value('vrata', val('Broj vrata'))
        vozilo_loader.add_value('boja', val('Boja'))
        
        vozilo_loader.add_value('lokacija_prodavca', lokacije[self._vozilo_index])

        yield vozilo_loader.load_item()