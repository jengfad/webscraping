import scrapy
from grafeauction.items import AuctionItem

class GrafespiderSpider(scrapy.Spider):
    name = 'GrafeSpider'
    fn = 'https://www.grafeauction.com'
    start_urls = [fn + '/event/pier-1-distribution-center-groveport-day-1']

    def parse(self, response):
        for lot_card in response.xpath('//div[contains(@class, "lot-card fillbox")]')[:3]:
            url = lot_card.xpath('.//h3[@class = "lot-card__title"]//a/@href').extract_first()
            formatted_url = self.fn + url
            auction_item = AuctionItem()
            auction_item['url'] = formatted_url
            auction_item['sale_order'] = lot_card.xpath('.//span[contains(@class, "lot-card__sale-order__value")]/text()').extract_first()
            yield scrapy.Request(formatted_url, callback=self.parse_lotpage, meta={'auction_item': auction_item})
    
    def parse_lotpage(self, response):
        auction_item = response.meta.get('auction_item')
        auction_item['title_name'] = response.xpath('//h1[contains(@class, "lot-detail__title")]/text()').extract_first()
        auction_item['lot_number'] = response.xpath('//div[contains(text(), "Lot")]//strong/text()').extract_first()
        auction_item['quantity'] = response.xpath('//div[contains(text(), "Qty")]//strong/text()').extract_first()
        auction_item['high_bid'] = response.xpath('//span[contains(@class, "lot-detail__high-bid__value")]/text()').extract_first()
        auction_item['customer_id'] = response.xpath('//span[contains(@class, "lot-detail__high-bid__bidder")]/text()').extract_first()
        auction_item['event_info'] = response.xpath('//span[contains(@class, "event-type")]/text()').extract_first()
        auction_item['online_premium'] = response.xpath('//span[contains(@class, "event-rates-online")]/span[contains(@class, "event-rates__amount")]/text()').extract_first()
        auction_item['sales_tax'] = response.xpath('//span[contains(@class, "event-rates-sales-tax")]/span[contains(@class, "event-rates__amount")]/text()').extract_first()
        auction_item['image_urls'] = response.xpath('//div[@class = "carousel-item"]//img/@src').extract()
        yield auction_item





        