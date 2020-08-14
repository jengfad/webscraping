# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import CsvItemExporter
from itemadapter import ItemAdapter
from dcasearch.logger import Logger
from dcasearch.exporters import CustomCsvItemExporter

class CustomSearchItemPipeline:
    def process_item(self, item, spider):
        self.write_item_to_file(item)
        return item

    def write_item_to_file(self, item):
        main_name = item.get('main_name')
        no_result_text=""
        if not main_name:
            no_result_text="-NoResult"
        path = 'output/ChiroCorporation/ChiroCorporation%s%s.csv' %(item.get('main_license_number'), no_result_text)
        self.file = open(path, 'w+b')
        self.exporter = CustomCsvItemExporter(self.file)
        self.exporter.start_exporting()
        self.exporter.export_item(item)
        self.exporter.finish_exporting()
        self.file.close()
        Logger.log('Finished Exporting')