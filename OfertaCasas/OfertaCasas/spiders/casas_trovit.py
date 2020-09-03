import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class casas_trovit_Spider(CrawlSpider):
    name = 'inmuebles24'
    allowed_domain = ['casas.trovit.com.mx']
    start_urls = ['https://casas.trovit.com.mx/casa-colima']

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="paginate"]/a[@data-test]'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//h4[@itemprop]')),
             callback='parse_item', follow=False)
    }

    def start_requests(self):
        urls = ['https://casas.trovit.com.mx/casa-colima']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contenedor = response.xpath('//div[contains(@class,"item") and contains(@class,"js-item")]')
