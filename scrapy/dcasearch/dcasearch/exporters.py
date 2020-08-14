from scrapy.exporters import CsvItemExporter
from dcasearch.logger import Logger

class CustomCsvItemExporter(CsvItemExporter):
    def export_item(self, item):
        Logger.log('Exporting')