# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import csv
from db.db import MysqlDAO
from scraper.scraper import settings

class MySQLStorePipeline:
    def __init__(self):
        self._db = MysqlDAO("vozila")
        
    def process_item(self, item, spider):
        self._db.save_vozilo(item)
        
        with open(settings.csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow([item[key] for key in item.keys()])
        return item
    