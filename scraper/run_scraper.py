from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
from scraper.scraper.spiders.vozilo import VoziloSpider

class Scraper:
    def __init__(self):
        settings_file_path = 'scraper.scraper.settings' # The path seen from root, i.e. a directory above
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = VoziloSpider
        
    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start()
        