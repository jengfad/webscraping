import scrapy
from hipages.items import ElectricianItem
from scrapy.loader import ItemLoader

class ElectricianspiderSpider(scrapy.Spider):
    name = 'ElectricianSpider'
    fn = 'https://hipages.com.au'
    start_urls = [fn + '/find/electricians/nsw/sydney']

    def parse(self, response):
        for index, card in enumerate(response.xpath('//div[contains(@class, "business-listing-header__BusinessListingHeaderColumn")]')): 
            
            if (index > 5):
                break
            
            url = self.fn + card.xpath('.//a/@href').extract_first()
            electrician_item = ElectricianItem()
            electrician_item_loader = ItemLoader(item=electrician_item, selector=card)
            electrician_item_loader.add_value('url', url)
            electrician_item_loader.load_item()

            yield scrapy.Request(url, callback=self.parse_electricianpage, meta={'electrician_item': electrician_item})

    def parse_electricianpage(self, response):
        electrician_item = response.meta.get('electrician_item')

        electrician_item_loader = ItemLoader(item=electrician_item, selector=response)
        electrician_item_loader.add_xpath('phone', './/span[contains(@class, "Contact__Item")]//img[contains(@src, "phone")]/following-sibling::span//a[contains(@class, "PhoneNumber__DesktopOnly")]/text()')
        electrician_item_loader.add_xpath('mobile', './/span[contains(@class, "Contact__Item")]//img[contains(@src, "mobile")]/following-sibling::span//a[contains(@class, "PhoneNumber__DesktopOnly")]/text()')
        electrician_item_loader.add_xpath('fax', './/span[contains(@class, "Contact__Item")]//img[contains(@src, "fax")]/following-sibling::span//a[contains(@class, "PhoneNumber__DesktopOnly")]/text()')
        electrician_item_loader.add_xpath('business_name', './/div[contains(@class, "Header__NameBlock")]//h1/text()')
        electrician_item_loader.add_xpath('contact_name', './/img[contains(@src, "contact")]/parent::span[contains(@class, "Contact__Item")]/text()[1]')
        electrician_item_loader.add_xpath('location', './/img[contains(@src, "loc")]/parent::span[contains(@class, "Contact__Item")]/text()[1]')
        electrician_item_loader.load_item()

        yield electrician_item
