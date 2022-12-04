import scrapy
import pandas as pd

class PltSpider(scrapy.Spider):
    name = 'plt'
    start_urls = ['https://www.prettylittlething.com/clothing.html?id=65&ajax=0']
    product_count = 0

    def parse(self, response):
        css_selector = 'a.product-url.js-click-product.js-category-product__link'
        products = response.css(css_selector)
                
        product_info = []
        for product in products:
            
            #Only scrape a maximum of 250 products
            self.product_count += 1

            #fetch price of product
            price = product.css('span.price::text').get()
            if price:
                price = price.replace('£', '')            
            #fetch product image
            image = product.css('div.product-image-block img::attr(data-src)').get()
            
            #fetch image name
            name = product.css('h2.product-title::text').get()
            if name:
                name = name.strip()
            
            info = {'name': name, 'price': price, 'image': image}
            product_info.append(info)
            
            yield info

        #Create pandas datdrame and write to db
        x = pd.DataFrame(product_info)
        print(x)

        next_page = response.css('a.load-more-btn::attr(href)').get()
        if next_page is not None and self.product_count < 250:
            yield response.follow(next_page, callback=self.parse)