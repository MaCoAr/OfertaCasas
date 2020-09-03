from scrapy.spiders import CrawlSpider

class inmuebles24_Spider(CrawlSpider):
    name = 'inmuebles'
    allowed_domain = ['www.inmuebles24.com']
    start_urls = ['https://www.inmuebles24.com/casas-en-venta-en-manzanillo.html']
