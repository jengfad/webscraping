# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose

class SearchItem(Item):
    main_name = Field(output_processor=TakeFirst())
    main_license_number = Field(output_processor=TakeFirst())
    main_license_type = Field(output_processor=TakeFirst()) 
    main_license_status = Field(output_processor=TakeFirst()) 
    main_address = Field(output_processor=TakeFirst())

    relation_name = Field(output_processor=TakeFirst())
    relation_license_number = Field(output_processor=TakeFirst())
    relation_license_type = Field(output_processor=TakeFirst())
    relation_license_status = Field(output_processor=TakeFirst())
    relation_address = Field(output_processor=TakeFirst())