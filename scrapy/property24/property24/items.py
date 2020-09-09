# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class PropertyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
        
    listingName = Field()
    totalPrice = Field()
    listingAddress = Field()
    listingUrl = Field()
