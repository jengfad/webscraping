# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose

class SearchItem(Item):
    name = Field(output_processor=TakeFirst())
    licenseNumber = Field(output_processor=TakeFirst())
    licenseType = Field(output_processor=TakeFirst()) 
    licenseStatus = Field(output_processor=TakeFirst()) 
    address = Field(output_processor=TakeFirst())