from ..items import NekretninaItem
from scrapy.loader.processors import TakeFirst
from itemloaders import ItemLoader
import scrapy


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
        nekretnina_loader = ItemLoader(item=NekretninaItem(), selector=response)
        
        nekretnina_loader.default_output_processor = TakeFirst()
        
        nekretnina_loader.add_css('naslov', 'h1.detail-title::text')
        nekretnina_loader.add_css('cena', 'h2.stickyBox__price::text')
        
        yield nekretnina_loader.load_item()