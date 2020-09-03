import scrapy
from transit.items import TransitItem

class CaTransitSpiderSpider(scrapy.Spider):
    name = 'ca_transit_spider'
    allowed_domains = ['home.cc.umanitoba.ca']
    fn = 'https://home.cc.umanitoba.ca/~wyatt/alltime'
    start_urls = ['https://home.cc.umanitoba.ca/~wyatt/alltime/bc.html']

    def parse(self, response):

        # test = response.xpath('//table[position()=1]//a/@href').get()
        # print('test')
        # print(test)

        for url in response.xpath('//table[position()=1]//a/@href').getall():
            yield scrapy.Request(url=self.fn + '/' + url, callback=self.parse_history_page)

    def parse_history_page(self, response):
        for index, header in enumerate(response.xpath('//b[contains(text(),"- present")]')):
            # print(header)
            # pass
            # print(index)
            name = header.xpath('.//i/text()').extract_first()

            if not name:
                continue

            date = header.xpath('.//i/../text()').extract_first().strip()

            if not date:
                raw = header.xpath('.//text()').extract_first()
                date = raw.replace(name, '')

            transit_item = TransitItem()
            transit_item['name'] = name
            transit_item['date'] = date.strip()

            yield transit_item