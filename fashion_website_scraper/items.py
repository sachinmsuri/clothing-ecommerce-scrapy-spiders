# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FashionWebsiteScraperItem(scrapy.Item):
    pass

class ClothingItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    sizes = scrapy.Field()
    link = scrapy.Field()

