# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import ClothingItem
import pymongo
import sys

class FashionWebsiteScraperPipeline:
    #pass
    collection = 'plt-items'

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db

        # if not self.mongodb_uri:
        #    sys.exit('No connection string has been provided')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri='mongodb+srv://admin:welcome1234@test-cluster.laxybot.mongodb.net/test', #crawler.settings.get('MONGODB_URI'),
            mongodb_db='scraped-clothing-website' #crawler.settings.get('MONGODB_DATABASE') #'items')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        self.db[self.collection].delete_many({})
    
    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        data = dict(ClothingItem(item))
        self.db[self.collection].insert_one(data)
        return item
