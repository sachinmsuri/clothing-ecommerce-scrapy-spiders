import scrapy
import pandas as pd
from scrapy import Request
from ..items import ClothingItem

class ZaraSpider(scrapy.Spider):
    name = 'zara'
    start_urls = ['https://www.zara.com/uk/en/woman-event-l1053.html?v1=1598203']
    product_count = 0

    def parse(self, response):
        css_selector = 'section.product-grid'
        products = response.css(css_selector)
        
        for product in products:
            print(product)
            self.product_count += 1
            redirect_link = product.css(
                'a.product-link.product-grid-product__link.link::attr(href)'
            ).get()
            print(redirect_link)
            print()

            yield Request(
                redirect_link, 
                callback=self.parse_product, 
                meta={'link': redirect_link}
            )
            break
        
    def parse_product(self, response):
        css_selector = 'div.layout__content'
        details = response.css(css_selector)

        for detail in details:
            image = detail.css('section.product-detail-images.product-detail-view__images.product-detail-images--with-thumbnails::attr(src)').get()
            print(image)
            print()

        # next_page = response.css('a.load-more-btn::attr(href)').get()
        # if next_page is not None and self.product_count < 10:
        #    yield response.follow(next_page, callback=self.parse)