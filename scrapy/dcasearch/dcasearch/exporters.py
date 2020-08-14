from scrapy.exporters import CsvItemExporter
from dcasearch.logger import Logger

class CustomCsvItemExporter(CsvItemExporter):
    def export_item(self, item):
        Logger.log('Custom Exporting')

        fields = self._get_serialized_fields(item, default_value='',
                                             include_empty=True)
        Logger.log('Serialized Fields')
        print(fields)
        for field in fields:
            row = self.custom_build_row(field[0], field[1])
            self.csv_writer.writerow(row)

    def custom_build_row(self, field_name, value):
        return [field_name, value]

