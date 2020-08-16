# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class CoffeeItem(Item):
    url = Field()
    brand = Field()
    product_name = Field()
    rating = Field()
    number_of_ratings = Field()
    price = Field()
    qty = Field()
    serve_style = Field()
