import scrapy
from grafeauction.items import AuctionItem
from scrapy.loader import ItemLoader
import grafeauction.constants as constants

class GrafespiderSpider(scrapy.Spider):
    name = 'GrafeSpider'
    fn = 'https://www.grafeauction.com'

    def start_requests(self):
        for url in constants.START_URLS:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for lot_card in response.xpath('//div[contains(@class, "lot-card fillbox")]')[:3]:
            url = lot_card.xpath('.//h3[@class = "lot-card__title"]//a/@href').extract_first()
            formatted_url = self.fn + url

            auction_item = AuctionItem()
            auction_item_loader = ItemLoader(item=auction_item, selector=lot_card)
            auction_item_loader.add_value('url', formatted_url)
            auction_item_loader.add_xpath('title_name', './/h3[@class = "lot-card__title"]//a/text()')
            auction_item_loader.add_xpath('customer_id', './/span[@class = "lot-card__high-bid__bidder"]/text()')
            auction_item_loader.add_xpath('sale_order', './/span[contains(@class, "lot-card__sale-order__value")]/text()')
            auction_item_loader.load_item()

            yield scrapy.Request(formatted_url, callback=self.parse_lotpage, meta={'auction_item': auction_item})
    
    def parse_lotpage(self, response):
        detail = response.xpath('//div[@class="lot-detail"]')[0]
        auction_item = response.meta.get('auction_item')
        auction_item_loader = ItemLoader(item=auction_item, selector=detail)

        auction_item_loader.add_xpath('lot_number', './/div[contains(text(), "Lot")]//strong/text()')
        auction_item_loader.add_xpath('quantity', './/div[contains(text(), "Qty")]//strong/text()')
        auction_item_loader.add_xpath('event_info', './/span[contains(@class, "event-type")]/text()')
        auction_item_loader.add_xpath('online_premium', './/span[contains(@class, "event-rates-online")]/span[contains(@class, "event-rates__amount")]/text()')
        auction_item_loader.add_xpath('sales_tax', './/span[contains(@class, "event-rates-sales-tax")]/span[contains(@class, "event-rates__amount")]/text()')
        auction_item_loader.add_xpath('image_urls', '///div[@class = "carousel-item"]//img/@src')
        yield auction_item_loader.load_item()





        