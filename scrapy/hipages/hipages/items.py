# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from scrapy.loader.processors import TakeFirst, MapCompose


class ElectricianItem(Item):
    business_name = Field(output_processor=TakeFirst()) 
    location = Field(output_processor=TakeFirst()) 
    post_code = Field(output_processor=TakeFirst()) 
    contact_name = Field(output_processor=TakeFirst()) 
    phone = Field(output_processor=TakeFirst()) 
    mobile = Field(output_processor=TakeFirst()) 
    fax = Field(output_processor=TakeFirst()) 
    url = Field(output_processor=TakeFirst()) 
