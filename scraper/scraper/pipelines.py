# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from db.db import MysqlDAO

class MySQLStorePipeline:
    def __init__(self):
        self.db = MysqlDAO("vozila")
        
    def process_item(self, item, spider):
        self.db.save_vozilo(item)
        return item
