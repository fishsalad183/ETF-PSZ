# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from db.mysql import MysqlDAO
from itemadapter import ItemAdapter


class MySQLStorePipeline:
    def __init__(self):
        self.db = MysqlDAO("nekretnine")
        
    def process_item(self, item, spider):
        self.db.save_nekretnina(item)
        return item
