import re

from itemloaders.processors import MapCompose, TakeFirst
from ..items import NekretninaItem
from itemloaders import ItemLoader
import scrapy
import logging


class NekretnineSpider(scrapy.Spider):
    name = 'nekretnine'
    allowed_domains = ['nekretnine.rs']
    start_urls = ['https://www.nekretnine.rs/stambeni-objekti/lista/po-stranici/20/stranica/1/']


    def parse(self, response):
        nekretnina_page_links = response.css('h2.offer-title a::attr(href)')
        yield from response.follow_all(nekretnina_page_links, self.parse_nekretnina)
        
        # pagination_links = response.css('a.next-article-button::attr(href)')
        # if pagination_links is not None:
        #     yield from response.follow_all(pagination_links, self.parse)
        
        
    def parse_nekretnina(self, response):
        def remove_whitespace(text):
            return text.strip()
        
        def extract_ponuda(text):
            if re.search("prodaja", text, re.IGNORECASE):
                return "P"
            elif re.search("izdavanje", text, re.IGNORECASE):
                return "I"

        def only_numeric_characters(text):
            return re.sub("[^0-9]", "", text)

        def extract_tip(text):
            if re.search("stanovi", text):
                return "stan"
            elif re.search("kuce", text):
                return "kuca"
            elif re.search("sobe", text):
                return "soba"
            elif re.search("ostali", text):
                return "ostalo"
        
        nekretnina_loader = ItemLoader(item=NekretninaItem(), selector=response)
        
        nekretnina_loader.default_output_processor = TakeFirst()
        
        nekretnina_loader.add_css('naslov', 'h1.detail-title::text', MapCompose(remove_whitespace))
        # nekretnina_loader.add_css('ponuda', 'h2.detail-seo-subtitle::text', MapCompose(extract_ponuda))
        nekretnina_loader.add_xpath('ponuda', '/html/body/div[6]/div[7]/div/div[1]/div[3]/h2/text()', MapCompose(extract_ponuda))
        nekretnina_loader.add_xpath('cena', '/html/body/div[6]/div[7]/div/div[1]/div[3]/div/h4[1]/text()', MapCompose(only_numeric_characters))
        nekretnina_loader.add_value('tip', response.request.url, MapCompose(extract_tip))
        
        yield nekretnina_loader.load_item()