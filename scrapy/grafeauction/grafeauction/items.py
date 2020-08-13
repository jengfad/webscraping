# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AuctionItem(scrapy.Item):
    title_name = scrapy.Field()  
    url = scrapy.Field()
    customer_id = scrapy.Field()
    lot_number = scrapy.Field()
    sale_order = scrapy.Field()
    high_bid = scrapy.Field()
    quantity = scrapy.Field()
    event_info = scrapy.Field()
    online_premium = scrapy.Field()
    sales_tax = scrapy.Field()
    event_begins_ending = scrapy.Field()
    image_urls = scrapy.Field()

