import scrapy
from transit.items import TransitItem

class CaTransitSpiderSpider(scrapy.Spider):
    name = 'ca_transit_spider'
    allowed_domains = ['home.cc.umanitoba.ca']
    fn = 'https://home.cc.umanitoba.ca/~wyatt/alltime'
    start_urls = ['https://home.cc.umanitoba.ca/~wyatt/alltime/operators.html']
    crawled_urls = []

    def parse(self, response):

        # test = response.xpath('//table[position()=1]//a/@href').get()
        # print('test')
        # print(test)

        for index, href in enumerate(response.xpath('//ol//a/@href').getall()):


            # if index == 2:
            #     break

            # href = 'vancouver-bc.html'

            # if '#' in href:
            #     part_index = href.index('#')
            #     page_part = href[part_index:len(href)]
            #     href = href.replace(page_part, '')

            url = self.fn + '/' + href

            
            print(f'operator #{index}: {url}')

            # if (url in self.crawled_urls):
            #     print('already crawled ' + url)
            #     continue

            self.crawled_urls.append(url)
            yield scrapy.Request(url=url, callback=self.parse_history_page)

    def parse_history_page(self, response):
        for index, header in enumerate(response.xpath('//b')):
            
            print(f'header #{index}')

            date = "".join(header.xpath('./text()').getall()).strip()

            if 'PRESENT' not in date.upper():
                continue

            link = header.xpath('.//a')
            
            if link:
                name = "".join(link.xpath('.//i/text()').get()).strip()
            else:
                name = header.xpath('.//i[1]/text()').get()
                if not name:
                    name = name = header.xpath('.//..//i[1]/text()').get()

            transit_item = TransitItem()
            transit_item['name'] = name
            transit_item['date'] = date.strip().replace('(', '').replace(')', '')
            transit_item['url'] = response.url

            yield transit_item