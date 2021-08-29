import re

from itemloaders.processors import MapCompose, TakeFirst
from ..items import NekretninaItem
from itemloaders import ItemLoader
import scrapy
import logging


class NekretnineSpider(scrapy.Spider):
    name = 'nekretnine'
    allowed_domains = ['nekretnine.rs']
    start_urls = ['https://www.nekretnine.rs/stambeni-objekti/cena/_30000/lista/po-stranici/20/',
                  'https://www.nekretnine.rs/stambeni-objekti/cena/30001_70000/lista/po-stranici/20/',
                  'https://www.nekretnine.rs/stambeni-objekti/cena/70001_110000/lista/po-stranici/20/',
                  'https://www.nekretnine.rs/stambeni-objekti/cena/110001_200000/lista/po-stranici/20/',
                  'https://www.nekretnine.rs/stambeni-objekti/cena/200001_/lista/po-stranici/20/']

    def parse(self, response):
        nekretnina_page_links = response.css('h2.offer-title a::attr(href)')
        yield from response.follow_all(nekretnina_page_links, self.parse_nekretnina)
        
        pagination_links = response.css('a.next-article-button::attr(href)')
        if pagination_links is not None:
            yield from response.follow_all(pagination_links, self.parse)
        
        
    def parse_nekretnina(self, response):
        def extract_ponuda(text) -> str:
            if re.search("prodaja", text, re.IGNORECASE):
                return "P"
            elif re.search("izdavanje", text, re.IGNORECASE):
                return "I"

        def only_numeric_characters(text) -> str:
            return re.sub("[^0-9]", "", text)

        def no_intervals(text) -> str:
            if "-" not in text:
                return only_numeric_characters(text)
            else:
                return None

        def extract_tip(text):
            if re.search("stanovi", text):
                return "stan"
            elif re.search("kuce", text):
                return "kuca"
            elif re.search("sobe", text):
                return "soba"
            elif re.search("ostali", text):
                return "ostalo"
        
        def to_boolean(text):
            if re.match("da", text, re.IGNORECASE):
                return True
            elif re.match("ne", text, re.IGNORECASE):
                return False
        
        nekretnina_loader = ItemLoader(item=NekretninaItem(), selector=response)
        
        nekretnina_loader.default_output_processor = TakeFirst()
        
        nekretnina_loader.add_value('url', response.request.url)
        nekretnina_loader.add_xpath('naslov', '/html/body/div[6]/div[7]/div/div[1]/h1/text()', MapCompose(lambda text: text.strip()))
        nekretnina_loader.add_xpath('ponuda', '/html/body/div[6]/div[7]/div/div[1]/div[3]/h2/text()', MapCompose(extract_ponuda))
        nekretnina_loader.add_xpath('cena', '/html/body/div[6]/div[7]/div/div[1]/div[3]/div/h4[1]/text()', MapCompose(no_intervals))
        nekretnina_loader.add_value('tip', response.request.url, MapCompose(extract_tip))
        nekretnina_loader.add_xpath('grad', '/html/body/div[6]/div[7]/div/div[1]/div[3]/h3/text()', MapCompose(lambda text: text.split(", ")[0].strip()))
        nekretnina_loader.add_xpath('deo_grada', '/html/body/div[6]/div[7]/div/div[1]/div[3]/h3/text()', MapCompose(lambda text: text.split(", ")[1].strip() if len(text.split(", ")) > 1 else None))
        nekretnina_loader.add_xpath('kvadratura', '/html/body/div[6]/div[7]/div/div[1]/div[3]/div/h4[2]/text()', MapCompose(no_intervals))
        nekretnina_loader.add_xpath('parking', '/html/body/div[6]/div[7]/div/div[1]/div[6]/div/ul/li[4]/span/text()', MapCompose(to_boolean))
        
        podaci_keys = response.xpath('/html/body/div[6]/div[7]/div/div[1]/section[1]/div[1]/ul/li/text()').extract()
        podaci_keys = map(lambda text: text.replace(":", "").strip(), podaci_keys)
        podaci_keys = filter(lambda text: text != "", podaci_keys)
        podaci_values = response.xpath('/html/body/div[6]/div[7]/div/div[1]/section[1]/div[1]/ul/li/strong/text()').extract()
        podaci_values = map(str.strip, podaci_values)
        podaci = dict(zip(podaci_keys, podaci_values))
        
        nekretnina_loader.add_value('stanje', podaci.get('Stanje nekretnine'))
        nekretnina_loader.add_value('godina_izgradnje', podaci.get('Godina izgradnje'))
        nekretnina_loader.add_value('povrsina_zemljista', only_numeric_characters(podaci.get('Površina zemljišta')) if podaci.get('Površina zemljišta') is not None else None)
        nekretnina_loader.add_value('sprat', podaci.get('Spratnost'))
        nekretnina_loader.add_value('spratnost', podaci.get('Ukupan broj spratova'))
        nekretnina_loader.add_value('opremljenost', podaci.get('Opremljenost nekretnine'))
        nekretnina_loader.add_value('uknjizeno', to_boolean(podaci.get('Uknjiženo')) if podaci.get('Uknjiženo') is not None else None)
        nekretnina_loader.add_value('broj_soba', podaci.get('Ukupan broj soba'))
        nekretnina_loader.add_value('broj_kupatila', podaci.get('Broj kupatila'))
        
        ostalo = {}
        for o in response.xpath('/html/body/div[6]/div[7]/div/div[1]/section[1]/div[5]/ul/li/text()').extract():
            spl = o.split(":")
            ostalo[spl[0].strip()] = spl[1].strip()
        nekretnina_loader.add_value('grejanje', ostalo.get('Grejanje'))
        
        dodatno = response.xpath('/html/body/div[6]/div[7]/div/div[1]/section[1]/div[2]/ul/li/text()').extract()
        nekretnina_loader.add_value('lift', True if "Lift" in dodatno else False)
        nekretnina_loader.add_value('terasa', True if "Terasa" in dodatno else False)
            
        yield nekretnina_loader.load_item()