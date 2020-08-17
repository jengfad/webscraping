# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class GrafeauctionPipeline:
    def process_item(self, item, spider):
        return item

class CustomImageNamePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for index, image_url in enumerate(item.get('image_urls', []), start = 1):
            yield scrapy.Request(
                image_url, 
                meta={
                    'lot_folder': item['lot_number'],
                    'index': index
                }
            )

    def file_path(self, request, response=None, info=None):
        return 'output/images/Lot %s/%s.jpg' % (request.meta['lot_folder'], request.meta['index'])