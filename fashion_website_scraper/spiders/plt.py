import scrapy
import pandas as pd
from scrapy import Request
from ..items import ClothingItem

class PltSpider(scrapy.Spider):
    name = 'plt'
    start_urls = ['https://www.prettylittlething.com/clothing.html?id=65&ajax=0']
    product_count = 0

    def parse(self, response):
        css_selector = 'a.product-url.js-click-product.js-category-product__link'
        products = response.css(css_selector)
        
        for product in products:
            self.product_count += 1
            redirect_link = product.css(
                'div.bv-content div::attr(data-bv-redirect-url)'
            ).get()
            yield Request(
                redirect_link, 
                callback=self.parse_product, 
                meta={'link': redirect_link}
            )

        next_page = response.css('a.load-more-btn::attr(href)').get()
        if next_page is not None and self.product_count < 250:
           yield response.follow(next_page, callback=self.parse)
    
    def parse_product(self, response):
        css_selector = 'div.main__content'
        details = response.css(css_selector)

        for detail in details:
            name = detail.css('h1.product-view-title::text').get()
            
            price = detail.css('span.price::text').get()
            if price:
                price = price.replace('£', '')

            image = detail.css('img.img-responsive::attr(src)').get()

            sizes = [size.strip() for size in 
                    detail.css('div.size-option:not(div.size-is-out-of-stock)::text').getall()]

            item = ClothingItem()
            
            item['name'] = name
            item['price'] = price
            item['image'] = image
            item['sizes'] = sizes
            item['link'] = response.meta.get('link')

            yield item

            # yield {
            #     'name': name,
            #     'price': price,
            #     'image': image,
            #     'sizes': sizes,
            #     'link': response.meta.get('link')
            # }