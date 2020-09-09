from scrapy import Request, Spider
from property24.items import PropertyItem



class PropertySpiderSpider(Spider):
    name = 'property_spider'
    allowed_domains = ['property24.com.ph']
    main_url = 'https://www.property24.com.ph/property-for-sale?ToPrice=1500000'
    fn = 'https://property24.com.ph/'

    def get_prefixed_url(self, href):
        return f'{self.fn}/{href}'

    def start_requests(self):
        for page_num in range(1):
            url = f'{self.main_url}&Page={page_num}'
            yield Request(url = url, callback = self.parse_page_list)


    def parse_page_list(self, response):
        for index, href in enumerate(response.xpath('//div[contains(@class, "sc_listingTile")]//div[contains(@class, "sc_listingTileContent")]/a[1]/@href').getall()):

            if index == 6:
                break

            url = self.get_prefixed_url(href)
            yield Request(url=url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        listingName = response.xpath('//div[contains(@class, "sc_listingAddress")]/h1/text()').get()
        totalPrice = response.xpath('//div[contains(@class, "p24_price")]/text()').get().replace('₱', '').strip()
        listingAddress = response.xpath('//div[contains(@class, "p24_listingCard p24_listingFeaturesWrapper")]/div[contains(@class, "p24_") and position() = 3]/p/text()').get().strip()

        property_item = PropertyItem()
        property_item['listingName'] = listingName
        property_item['totalPrice'] = totalPrice
        property_item['listingAddress'] = listingAddress
        property_item['listingUrl'] = response.url

        yield property_item