# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import replace_escape_chars

def trimmify(value):
    return value.strip()

def percentify(value):
    return value + '%'

class AuctionItem(Item):
    title_name = Field(
        input_processor=MapCompose(trimmify),
        output_processor=TakeFirst()
    )  
    url =  Field(output_processor=TakeFirst()) 
    customer_id = Field(
        input_processor=MapCompose(trimmify),
        output_processor=TakeFirst()
    )  
    lot_number = Field(output_processor=TakeFirst()) 
    sale_order = Field(output_processor=TakeFirst()) 
    high_bid = Field(output_processor=TakeFirst()) 
    quantity = Field(output_processor=TakeFirst()) 
    event_info = Field(output_processor=TakeFirst()) 
    online_premium = Field(
        input_processor=MapCompose(percentify),
        output_processor=TakeFirst()
    )  
    sales_tax = Field(
        input_processor=MapCompose(percentify),
        output_processor=TakeFirst()
    )  
    event_begins_ending = Field(output_processor=TakeFirst()) 
    image_urls = Field() 

