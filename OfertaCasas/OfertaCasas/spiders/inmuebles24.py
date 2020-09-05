import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OfertacasasItems

class Property24Spider(CrawlSpider):
    name = 'inmuebles'
    allowed_domain = ['www.inmuebles24.com']
    start_urls = ['https://www.inmuebles24.com/casas-en-venta-en-manzanillo.html']

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class="pag-go-next"]/a/i[@class="icon-g icon-g-chevron-right"]'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//h2[@class="posting-title"]/a')),
             callback='parse_item', follow=False)
    }

    def start_requests(self):
        urls = [
            'https://www.inmuebles24.com/casas-en-venta-en-manzanillo.html'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        container = response.xpath('//div[contains(@class,"posting-card")]')
        for i in range(len(container)):
            OfCa_Items = OfertacasasItems()
            OfCa_Items['house_id'] = container[i].xpath('//[@data-to-posting]').get()
            OfCa_Items['url'] = response.url
            OfCa_Items['location'] = container[i].xpath('//span[contains(@class,"posting-location")]/span/text()').get()
            OfCa_Items['description'] = container[i].xpath('//div[contains(@class,"posting-description")]/text()').get()
            OfCa_Items['bedrooms'] = container[i].xpath('//ul[contains(@class,"main-features")]/li[3]').get()
            OfCa_Items['baths'] = container[i].xpath('//ul[contains(@class,"main-features")]/li[4]').get()
            OfCa_Items['area'] = container[i].xpath('//ul[contains(@class,"main-features")]/li[1]').get()
            OfCa_Items['price'] = container[i].xpath('//div[contains(@class,"prices")]/span').get()
            OfCa_Items['garage'] = container[i].xpath('//ul[contains(@class,"main-features")]/li[5]').get()

            img_items = []
            selectorImages = container[i].xpath('//div[contains(@class,"flickity-slider")]')
            for j in range(1, len(selectorImages)):
                img = selectorImages.xpath('//div[contains(@class,"flickity-slider")]/div/img')[j].attrib['src']
                img_items.append(img)

            OfCa_Items['images'] = img_items

            yield OfCa_Items
