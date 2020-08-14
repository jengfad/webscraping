# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import CsvItemExporter
from itemadapter import ItemAdapter


class CustomSearchItemPipeline:
    def process_item(self, item, spider):
        self.write_item_to_file(item)
        return item

    def write_item_to_file(self, item):
        path = 'output/Chiro_%s.csv' %(item.get('licenseNumber'))
        self.file = open(path, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.export_item(item)